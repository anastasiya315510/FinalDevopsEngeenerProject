{{- define "grafana.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "grafana.fullname" -}}
{{ printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "grafana.namespace" -}}
{{ .Release.Namespace }}
{{- end }}

{{- define "grafana.labels" -}}
app.kubernetes.io/name: {{ include "grafana.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "grafana.selectorLabels" -}}
app.kubernetes.io/name: {{ include "grafana.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{- define "grafana.configData" -}}
{{- /* return a hash/checksum for configmaps or dashboards */ -}}
{{- end }}

{{- define "grafana.secretsData" -}}
{{- /* return hash/checksum for secrets */ -}}
{{- end }}

{{- define "grafana.pod" -}}
{{- /* pod spec, e.g., container image, env, ports */ -}}
{{- end }}
