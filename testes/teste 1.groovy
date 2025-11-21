import java.net.HttpURLConnection
import java.net.URL
import java.io.OutputStreamWriter
import java.util.Base64
import groovy.json.JsonOutput

//Inivializando variáveis do payload
def currentTaskInfoRaw = execution.getVariable("currentTaskInfo")
def currentTaskInfo = currentTaskInfoRaw ? new groovy.json.JsonSlurper().parse(currentTaskInfoRaw) : null
def endpoint = "https://apiexternaltask-production.up.railway.app/events/log"
def body = [
  currentTaskName: task.getVariable("taskCurrentActivityName") ?: "", // Nome da tarefa atual
  nextTaskName: task.getVariable("taskNextActivityName") ?: "", // Nome da próxima tarefa
  nextGroupName: task.getVariable("nextTaskGroupName") ?: "", // Nome do grupo destinatario
  nextGroupId: task.getVariable("next_groupId") ?: "", // ID do grupo destinatario
  senderUserName: currentTaskInfo?.taskAssignee ?: "", // Nome do usuário que está enviando
  senderUserId: currentTaskInfo?.taskAssigneeId ?: "", // ID do usuário que está enviando
  currentGroupName: currentTaskInfo?.groupName ?: "", // Nome do grupo que está enviando
  currentGroupId: currentTaskInfo?.groupId ?: "",// ID do grupo que está enviando
]

// Valida entrada de dados para coleta das variáveis
def wdywtdRaw = execution.getVariable("whatDoYouWantToDo") ?: ""
def wdywtd = (wdywtdRaw instanceof String) ? new JsonSlurper().parseText(wdywtdRaw) : wdywtdRaw
def wPType = wdywtd?.phaseExit?.type

if (wPType == 'External') {
  body['nextTaskName'] = task.getVariable("taskNextActivityName") ?: ""
  body['nextGroupName'] = null
  body['next_groupId'] = null
}
task.setVariable("payloadPost", body)



// converter o payload em string JSON
def jsonString = JsonOutput.toJson(body)


// Abre conexão POST
def connection = (HttpURLConnection) new URL(endpoint).openConnection()
connection.setRequestMethod("POST")
connection.setRequestProperty("Content-Type", "application/json")
connection.setDoOutput(true)

// Envia body
def writer = new OutputStreamWriter(connection.outputStream)
writer.write(jsonString)
writer.flush()
writer.close()

// Leitura do Status Code
def responseCode = connection.responseCode
if (responseCode >= 200 && responseCode < 300) {
    println "Log de eventos enviados com sucesso. Status: " + responseCode
    task.setVariable("hasSendEventsLogs", "true")
} else {
    // Se falhar, leia o stream de erro (para ver o 422/500)
    def errorStream = connection.errorStream
    def errorBody = errorStream ? new String(errorStream.readAllBytes()) : "N/A"
    
    println "ERRO ao enviar evento. Status: " + responseCode + ", Detalhe: " + errorBody
    task.setVariable("hasSendEventsLogs", "false")
}
connection.disconnect()



