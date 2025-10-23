{{/* Return the full name of the chart */}}
{{- define "flask-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Return the chart name */}}
{{- define "flask-chart.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{/* Common labels */}}
{{- define "flask-chart.labels" -}}
app.kubernetes.io/name: {{ include "flask-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
