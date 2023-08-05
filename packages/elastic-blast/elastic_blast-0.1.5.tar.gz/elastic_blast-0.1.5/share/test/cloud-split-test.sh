#!/bin/bash -e
# Bash script for EB-974, EB-1081
# Run share/test/cloud-split-test.sh s3://some-bucket disk-type
# where disk-type is either local-ssd or ebs
# Produces run summary files split-only-*-summary.json
# Uses config files share/etc/elb-aws-split-only-*.ini 
RESULTS_BUCKET=${1:-"s3://elasticblast-test"}
dt=${2:-local-ssd}

for ds in mane vht2 viralmeta; do
    cfg=share/etc/elb-aws-split-only-$dt-$ds.ini
    results=$RESULTS_BUCKET/cloud_split/split-only-$dt-$ds
    ELB_NO_SEARCH=1 ELB_USE_1_STAGE_CLOUD_SPLIT=1 elastic-blast submit --cfg $cfg --results $results
    elastic-blast status --wait --cfg $cfg --results $results
    elastic-blast run-summary --cfg $cfg --results $results --write-logs split-only-$dt-$ds.logs -o split-only-$dt-$ds-summary.json
    elastic-blast delete --cfg $cfg --results $results
done
