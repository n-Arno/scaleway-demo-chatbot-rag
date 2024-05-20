resource "random_password" "db" {
  length      = 10
  min_numeric = 1
  min_upper   = 1
  min_lower   = 1
  min_special = 1
}

resource "scaleway_rdb_instance" "vector" {
  name           = "vector"
  node_type      = "DB-DEV-S"
  engine         = "PostgreSQL-15"
  is_ha_cluster  = false
  disable_backup = true
  user_name      = "db_user"
  password       = random_password.db.result
  private_network {
    pn_id       = scaleway_vpc_private_network.kapsule.id
    enable_ipam = true
  }
  depends_on = [random_password.db, scaleway_vpc_gateway_network.kapsule]
}

resource "scaleway_rdb_acl" "private_only" {
  # default acl for DB is 0.0.0.0/0.
  # We can't delete it via terraform but we can replace it
  # with the local subnet (even if ACL is not used with PN)
  # to disable access via internet.
  instance_id = scaleway_rdb_instance.vector.id
  acl_rules {
    ip          = local.subnet
    description = "Private network access only"
  }
}

output "database_password" {
  value = nonsensitive(random_password.db.result)
}

data "scaleway_ipam_ip" "private_database_ip" {
  resource {
    id   = scaleway_rdb_instance.vector.id
    type = "rdb_instance"
  }
  type = "ipv4"
}

output "database_ip" {
  value = data.scaleway_ipam_ip.private_database_ip.address
}
