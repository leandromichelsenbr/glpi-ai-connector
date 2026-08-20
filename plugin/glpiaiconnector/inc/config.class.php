<?php

class PluginGlpiaiconnectorConfig extends CommonDBTM
{
    public static function getTypeName($nb = 0): string { return __('GLPI AI Connector', 'glpiaiconnector'); }
    public static function getConfig(): array { return Config::getConfigurationValues('plugin:glpiaiconnector'); }
    public static function canView(): bool { return Session::haveRight('config', READ); }
    public static function canUpdate(): bool { return Session::haveRight('config', UPDATE); }

    public static function save(array $input): void
    {
        if (!self::canUpdate()) { throw new RuntimeException('Sem permissão para alterar a configuração.'); }
        $allowed = ['enabled','allow_create','allow_update','allow_followup','allow_assignment','allow_status_change','allow_solution','allow_close','allowed_entities','gateway_url'];
        $values = [];
        foreach ($allowed as $key) {
            if (str_starts_with($key, 'allow_') || $key === 'enabled') {
                $values[$key] = isset($input[$key]) ? 1 : 0;
            } elseif (isset($input[$key])) {
                $values[$key] = trim((string)$input[$key]);
            }
        }
        Config::setConfigurationValues('plugin:glpiaiconnector', $values);
    }
}
