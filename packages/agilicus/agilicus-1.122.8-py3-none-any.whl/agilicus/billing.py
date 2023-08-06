import agilicus
from .input_helpers import get_org_from_input_or_ctx
from .context import get_apiclient_from_ctx
import operator

from .output.table import (
    column,
    spec_column,
    status_column,
    metadata_column,
    format_table,
    subtable,
)


def get_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.get_billing_account(billing_account_id, **kwargs)


def list_accounts(ctx, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.list_billing_accounts(**kwargs)


def format_accounts(ctx, accounts):
    orgs_column = [column("id"), column("organisation")]
    products_column = [
        column("name"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("customer_id"),
        spec_column("dev_mode"),
        status_column("customer", optional=True),
        subtable(ctx, "products", products_column, subobject_name="status"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
    ]
    return format_table(ctx, accounts, columns)


def add_billing_account(ctx, customer_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingAccountSpec(customer_id=customer_id)
    account = agilicus.BillingAccount(spec=spec)

    return client.billing_api.create_billing_account(account)


def add_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_account(
        billing_account_id, billing_org=billing_org
    )


def remove_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_account(billing_account_id, org_id)


def replace_billing_account(
    ctx, billing_account_id=None, customer_id=None, dev_mode=None, **kwargs
):
    client = get_apiclient_from_ctx(ctx)

    existing = client.billing_api.get_billing_account(billing_account_id)
    if customer_id is not None:
        existing.spec.customer_id = customer_id
    if dev_mode is not None:
        existing.spec.dev_mode = dev_mode
    return client.billing_api.replace_billing_account(
        billing_account_id, billing_account=existing
    )


def format_usage_records(ctx, records):
    columns = [
        column("id"),
        column("period"),
        column("total_usage"),
    ]
    return format_table(ctx, records, columns, getter=operator.itemgetter)


def get_usage_records(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_usage_records(billing_account_id)


def create_usage_record(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.add_billing_usage_record(billing_account_id)
