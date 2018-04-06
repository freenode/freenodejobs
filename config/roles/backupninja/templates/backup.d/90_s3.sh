trap "rm -rf /var/backups/postgres" EXIT

set -a
. {{ base_dir }}/.env
set +a

s3cmd \
	--verbose \
	--server-side-encryption \
	--storage-class=STANDARD_IA \
	sync \
	/var/backups/ \
	s3://freenodejobs-backup/$(hostname)/ || fatal s3cmd
