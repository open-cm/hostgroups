import os

apps = [
    "kubernetes", "openobserve", "prometheus", "grafana", "elasticsearch",
    "redis", "kafka", "nginx", "postgres", "mongodb",
    "rabbitmq", "vault", "consul", "traefik", "harbor",
    "argocd", "jenkins", "gitlab", "minio", "nextcloud", "zabbix"
]

mapping = {
    "kubernetes": ["control_plane", "worker"],
    "openobserve": ["ingester", "querier"],
    "prometheus": ["server", "node_exporter"],
    "grafana": ["server"],
    "elasticsearch": ["master", "data"],
    "redis": ["master", "replica"],
    "kafka": ["broker", "zookeeper"],
    "nginx": ["proxy"],
    "postgres": ["primary", "standby"],
    "mongodb": ["shard", "config"],
    "rabbitmq": ["cluster"],
    "vault": ["server"],
    "consul": ["server", "agent"],
    "traefik": ["controller"],
    "harbor": ["core", "registry"],
    "argocd": ["server", "controller"],
    "jenkins": ["master", "agent"],
    "gitlab": ["app", "runner"],
    "minio": ["server"],
    "nextcloud": ["app"],
    "zabbix": ["server", "agent", "proxy"]
}

# Define OS support
os_support = {
    "kubernetes": ["Linux"], # Control plane/Nodes primary on Linux
    "openobserve": ["Linux"],
    "prometheus": ["Linux", "Windows"],
    "grafana": ["Linux", "Windows"],
    "elasticsearch": ["Linux", "Windows"],
    "redis": ["Linux"], # Core redis is Linux
    "kafka": ["Linux", "Windows"],
    "nginx": ["Linux", "Windows"],
    "postgres": ["Linux", "Windows"],
    "mongodb": ["Linux", "Windows"],
    "rabbitmq": ["Linux", "Windows"],
    "vault": ["Linux", "Windows"],
    "consul": ["Linux", "Windows"],
    "traefik": ["Linux", "Windows"],
    "harbor": ["Linux"],
    "argocd": ["Linux"],
    "jenkins": ["Linux", "Windows"],
    "gitlab": ["Linux"],
    "minio": ["Linux", "Windows"],
    "nextcloud": ["Linux"],
    "zabbix": ["Linux", "Windows"]
}

hgs = []

# Base
hgs.append(f"""  - name: Base
    puppetclasses:
      - base
    fact_rules: []""")

# OS levels
for os_name in ["Linux", "Windows"]:
    kernel_val = "Linux" if os_name == "Linux" else "windows"
    hgs.append(f"""  - name: Base/{os_name}
    puppetclasses:
      - base::{os_name.lower()}
    fact_rules:
      - fact: kernel
        operator: "="
        value: {kernel_val}""")
    
    # Apps levels
    for app in apps:
        # Check if app supports current OS
        if os_name not in os_support.get(app, ["Linux"]):
            continue

        hgs.append(f"""  - name: Base/{os_name}/{app.capitalize()}
    puppetclasses:
      - {app}
    fact_rules:
      - fact: app
        operator: "="
        value: {app}""")
        
        # Features/Components levels
        features = mapping.get(app, ["default"])
        for feature in features:
            hgs.append(f"""  - name: Base/{os_name}/{app.capitalize()}/{feature.capitalize().replace('_', '')}
    puppetclasses:
      - {app}::{feature}
    fact_rules:
      - fact: app_feature
        operator: "="
        value: {feature}""")

output = "hostgroups:\n" + "\n".join(hgs)

with open('hostgroups.yaml', 'w') as f:
    f.write(output)
