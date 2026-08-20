<?php

function plugin_glpiaiconnector_install(): bool
{
    global $DB;
    $migration = new Migration(100);

    if (!$DB->tableExists('glpi_plugin_glpiaiconnector_audits')) {
        $query = <<<SQL
CREATE TABLE `glpi_plugin_glpiaiconnector_audits` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `users_id` int unsigned NOT NULL DEFAULT 0,
    `agent_name` varchar(255) DEFAULT NULL,
    `operation` varchar(100) NOT NULL,
    `itemtype` varchar(100) DEFAULT NULL,
    `items_id` int unsigned DEFAULT NULL,
    `success` tinyint NOT NULL DEFAULT 1,
    `details` text DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `operation` (`operation`),
    KEY `item` (`itemtype`, `items_id`),
    KEY `date_creation` (`date_creation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SQL;
        $DB->query($query);
    }

    $defaults = [
        'enabled' => 0,
        'allow_create' => 1,
        'allow_update' => 1,
        'allow_followup' => 1,
        'allow_assignment' => 1,
        'allow_status_change' => 1,
        'allow_solution' => 1,
        'allow_close' => 0,
        'allowed_entities' => '',
        'gateway_url' => '',
    ];

    $current = Config::getConfigurationValues('plugin:glpiaiconnector');
    foreach ($defaults as $key => $value) {
        if (!array_key_exists($key, $current)) {
            Config::setConfigurationValues('plugin:glpiaiconnector', [$key => $value]);
        }
    }

    $migration->executeMigration();
    return true;
}

function plugin_glpiaiconnector_uninstall(): bool
{
    global $DB;
    if ($DB->tableExists('glpi_plugin_glpiaiconnector_audits')) {
        $DB->query('DROP TABLE `glpi_plugin_glpiaiconnector_audits`');
    }
    Config::deleteConfigurationValues('plugin:glpiaiconnector');
    return true;
}
