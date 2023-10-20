"""
# Integration test for Cost Optimization Data Collection

## About
    This test will:
    - deploy Cost Optimization Data Collection stacks (all in one account)
    - update all nested stacks to the git version
    - trigger collection
    - test that collection works  (tables are not empty)
    - delete all stacks and tables

## Prerequisites in account:
    1. Activate Organizations
    2. Opt-In Compute Optimizer
    3. Activate Business or Enterprise Support (for ta collection only)
    4. Create:
        RDS instance, Budget, Unattached EBS, ECS cluster with at least 1 Service,
    FIXME: add CFM for Prerequisites

## Install:
    pip3 install cfn-flip boto3 pytest

## Run (expect 15 mins):
Pytest:

    pytest

Python:
    python3 Test/test-from-scratch.py


"""
import logging

import pytest

from utils import athena_query


logger = logging.getLogger(__name__)



def test_budgets_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."budgets_data" LIMIT 10;')
    assert len(data) > 0, 'budgets_data is empty'


def test_cost_explorer_rightsizing_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."cost_explorer_rightsizing_data" LIMIT 10;')
    assert len(data) > 0, 'cost_explorer_rightsizing_data is empty'


def test_cost_anomaly_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."cost_anomaly_data" LIMIT 10;')
    assert len(data) > 0, 'cost_anomaly_data is empty'


def test_ecs_chargeback_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."ecs_chargeback_data" LIMIT 10;')
    assert len(data) > 0, 'ecs_chargeback_data is empty'


def test_inventory_ami_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_ami_data" LIMIT 10;')
    assert len(data) > 0, 'inventory_ami_data is empty'


def test_inventory_ebs_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_ebs_data" LIMIT 10;')
    assert len(data) > 0, 'inventory_ebs_data is empty'


def test_inventory_snapshot_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_snapshot_data" LIMIT 10;')
    assert len(data) > 0, 'inventory_snapshot_data is empty'


def test_rds_usage_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."rds_usage_data" LIMIT 10;')
    assert len(data) > 0, 'rds_usage_data is empty'

def test_organization_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."organization_data" LIMIT 10;')
    assert len(data) > 0, 'organization_data is empty'

def test_trusted_advisor_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."trusted_advisor_data" LIMIT 10;')
    assert len(data) > 0, 'trusted_advisor_data is empty'


def test_transit_gateway_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."transit_gateway_data" LIMIT 10;')
    assert len(data) > 0, 'transit_gateway_data is empty'


def test_opensearch_domains_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_opensearch_domains_data" LIMIT 10;')
    assert len(data) > 0, 'opensearch_domains_data is empty'


def test_elasticache_clusters_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_elasticache_clusters_data" LIMIT 10;')
    assert len(data) > 0, 'elasticache_clusters_data is empty'


def test_rds_db_instances_data(athena):
    data = athena_query(athena=athena, sql_query='SELECT * FROM "optimization_data"."inventory_rds_db_instances_data" LIMIT 10;')
    assert len(data) > 0, 'rds_db_instances_data is empty'


def test_compute_optimizer_export_triggered(compute_optimizer, start_time):
    jobs = compute_optimizer.describe_recommendation_export_jobs()['recommendationExportJobs']
    logger.debug(f'Jobs in: {jobs}')
    jobs_since_start = [job for job in jobs if job['creationTimestamp'].replace(tzinfo=None) > start_time.replace(tzinfo=None)]
    assert len(jobs_since_start) == 5, f'started {len(jobs_since_start)} jobs. Expected 5. Not all jobs launched'
    jobs_failed = [job for job in jobs_since_start if job.get('status') == 'failed']
    assert len(jobs_failed) == 0, f'Some jobs failed {jobs_failed}'
    # TODO: check how we can add better test, taking into account 15-30 mins delay of export in CO

if __name__ == '__main__':
    pytest.main()