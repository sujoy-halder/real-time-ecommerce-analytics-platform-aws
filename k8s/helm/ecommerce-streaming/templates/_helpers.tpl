{{- define "ecommerce-streaming.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ecommerce-streaming.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "ecommerce-streaming.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ecommerce-streaming.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "ecommerce-streaming.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{- define "ecommerce-streaming.labels" -}}
app.kubernetes.io/name: {{ include "ecommerce-streaming.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

