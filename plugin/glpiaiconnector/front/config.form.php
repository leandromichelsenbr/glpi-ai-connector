<?php

include('../../../inc/includes.php');
Session::checkRight('config', UPDATE);
if (isset($_POST['update'])) {
    PluginGlpiaiconnectorConfig::save($_POST);
    Session::addMessageAfterRedirect(__('Configuração salva.', 'glpiaiconnector'), true, INFO);
}
Html::back();
