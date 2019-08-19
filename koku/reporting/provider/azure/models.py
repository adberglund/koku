#
# Copyright 2019 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Models for Azure cost and usage entry tables."""

from django.contrib.postgres.fields import JSONField
from django.db import models


class AzureCostEntryBill(models.Model):
    """The billing information for a Cost Usage Report.

    The billing period (1 month) will cover many cost entries.

    """

    class Meta:
        """Meta for AzureBill."""

        unique_together = ('subscription_guid', 'billing_period_start',
                           'provider_id')

    subscription_guid = models.CharField(max_length=50, null=False)
    billing_period_start = models.DateTimeField(null=False)
    billing_period_end = models.DateTimeField(null=False)
    summary_data_creation_datetime = models.DateTimeField(null=True)
    summary_data_updated_datetime = models.DateTimeField(null=True)
    finalized_datetime = models.DateTimeField(null=True)
    derived_cost_datetime = models.DateTimeField(null=True)

    # provider_id is intentionally not a foreign key
    # to prevent masu complication
    provider_id = models.IntegerField(null=True)


class AzureCostEntryProduct(models.Model):
    """The Azure product identified in a cost entry line item."""

    class Meta:
        """Meta for AzureCostEntryProduct."""

        unique_together = ('instance_id', 'resource_location')

        indexes = [
            models.Index(
                fields=['resource_location'],
                name='resource_location_idx',
            ),
        ]
    instance_id = models.CharField(max_length=512, null=False)
    resource_location = models.CharField(max_length=50, null=False)
    consumed_service = models.CharField(max_length=50, null=False)
    resource_type = models.CharField(max_length=50, null=False)
    resource_group = models.CharField(max_length=50, null=False)


class AzureMeter(models.Model):
    """The Azure meter."""

    class Meta:
        """Meta for AzureMeter."""

        unique_together = ('meter_id', 'meter_category', 'meter_region')

    meter_id = models.CharField(max_length=50, null=False)
    meter_name = models.CharField(max_length=50, null=False)
    meter_category = models.CharField(max_length=50, null=True)
    meter_subcategory = models.CharField(max_length=50, null=True)
    meter_region = models.CharField(max_length=50, null=True)


class AzureService(models.Model):
    """The Azure service."""

    class Meta:
        """Meta for AzureMeter."""

        unique_together = ('service_tier', 'service_name')

    service_tier = models.CharField(max_length=50, null=False)
    service_name = models.CharField(max_length=50, null=False)
    service_info1 = models.CharField(max_length=50, null=True)
    service_info2 = models.CharField(max_length=50, null=True)


class AzureCostEntryLineItem(models.Model):
    """A line item in a cost entry.

    This identifies specific costs and usage of Azure resources.

    """

    id = models.BigAutoField(primary_key=True)

    cost_entry_bill = models.ForeignKey('AzureCostEntryBill',
                                        on_delete=models.PROTECT)

    cost_entry_product = models.ForeignKey('AzureCostEntryProduct',
                                           on_delete=models.PROTECT, null=True)

    meter = models.ForeignKey('AzureMeter',
                              on_delete=models.PROTECT, null=True)

    service = models.ForeignKey('AzureService',
                                on_delete=models.PROTECT, null=True)

    tags = JSONField(null=True)

    additional_info = JSONField(null=True)

    usage_date_time = models.DateTimeField(null=False)

    usage_quantity = models.DecimalField(max_digits=24, decimal_places=9,
                                         null=True)

    resource_rate = models.DecimalField(max_digits=17, decimal_places=9,
                                        null=True)

    pretax_cost = models.DecimalField(max_digits=17, decimal_places=9,
                                      null=True)

    offer_id = models.PositiveIntegerField(null=True)
