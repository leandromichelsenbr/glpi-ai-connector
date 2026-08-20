<?php

include('../../../inc/includes.php');
Session::checkRight('config', READ);
Html::header(__('GLPI AI Connector', 'glpiaiconnector'), $_SERVER['PHP_SELF'], 'config', 'plugins');
$config = PluginGlpiaiconnectorConfig::getConfig();

echo "<div class='center'><h2>GLPI AI Connector</h2><p>Configure quais operações os agentes de IA poderão solicitar através do gateway.</p></div>";
echo "<form method='post' action='config.form.php'><table class='tab_cadre_fixe'>";
echo "<tr><th colspan='2'>Configuração geral</th></tr>";
echo "<tr class='tab_bg_1'><td>Integração habilitada</td><td>"; Dropdown::showYesNo('enabled', (int)($config['enabled'] ?? 0)); echo "</td></tr>";
echo "<tr class='tab_bg_1'><td>URL do Gateway</td><td><input type='url' name='gateway_url' size='70' value='" . Html::cleanInputText($config['gateway_url'] ?? '') . "'></td></tr>";
echo "<tr class='tab_bg_1'><td>Entidades permitidas</td><td><input type='text' name='allowed_entities' size='40' value='" . Html::cleanInputText($config['allowed_entities'] ?? '') . "'><br><small>IDs separados por vírgula. Vazio = sem restrição adicional.</small></td></tr>";
echo "<tr><th colspan='2'>Operações permitidas</th></tr>";
$operations = ['allow_create'=>'Criar tickets','allow_update'=>'Atualizar tickets','allow_followup'=>'Adicionar acompanhamentos','allow_assignment'=>'Atribuir técnico','allow_status_change'=>'Alterar status','allow_solution'=>'Registrar solução','allow_close'=>'Fechar tickets'];
foreach ($operations as $key => $label) {
    echo "<tr class='tab_bg_1'><td>{$label}</td><td>"; Dropdown::showYesNo($key, (int)($config[$key] ?? 0)); echo "</td></tr>";
}
if (PluginGlpiaiconnectorConfig::canUpdate()) {
    echo "<tr class='tab_bg_2'><td colspan='2' class='center'><button type='submit' name='update' class='btn btn-primary'>Salvar</button></td></tr>";
}
echo "</table>";
Html::closeForm();
echo "<div class='center' style='margin-top:20px'><p><strong>Observação:</strong> nesta versão o plugin administra política e auditoria. O gateway MCP continua sendo executado como serviço externo.</p></div>";
Html::footer();
