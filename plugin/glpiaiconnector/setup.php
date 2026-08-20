<?php

define('PLUGIN_GLPIAICONNECTOR_VERSION', '0.1.0');
define('PLUGIN_GLPIAICONNECTOR_MIN_GLPI', '10.0.0');
define('PLUGIN_GLPIAICONNECTOR_MAX_GLPI', '10.0.99');

function plugin_init_glpiaiconnector(): void
{
    global $PLUGIN_HOOKS;
    $PLUGIN_HOOKS['csrf_compliant']['glpiaiconnector'] = true;
    $PLUGIN_HOOKS['config_page']['glpiaiconnector'] = 'front/config.php';
    Plugin::registerClass('PluginGlpiaiconnectorConfig', ['addtabon' => 'Config']);
}

function plugin_version_glpiaiconnector(): array
{
    return [
        'name' => 'GLPI AI Connector',
        'version' => PLUGIN_GLPIAICONNECTOR_VERSION,
        'author' => 'USINA.BR Tecnologia e Informação Ltda.',
        'license' => 'MIT',
        'homepage' => 'https://github.com/leandromichelsenbr/glpi-ai-connector',
        'requirements' => ['glpi' => ['min' => PLUGIN_GLPIAICONNECTOR_MIN_GLPI, 'max' => PLUGIN_GLPIAICONNECTOR_MAX_GLPI]],
    ];
}

function plugin_glpiaiconnector_check_prerequisites(): bool
{
    if (version_compare(GLPI_VERSION, PLUGIN_GLPIAICONNECTOR_MIN_GLPI, '<')) {
        echo 'GLPI AI Connector requer GLPI ' . PLUGIN_GLPIAICONNECTOR_MIN_GLPI . ' ou superior.';
        return false;
    }
    return true;
}

function plugin_glpiaiconnector_check_config(bool $verbose = false): bool
{
    return true;
}
