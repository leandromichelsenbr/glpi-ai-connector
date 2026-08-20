<?php

class PluginGlpiaiconnectorAudit extends CommonDBTM
{
    public static $rightname = 'config';
    public static function getTypeName($nb = 0): string { return __('Auditoria GLPI AI Connector', 'glpiaiconnector'); }

    public static function record(string $operation, ?string $itemtype = null, ?int $itemsId = null, bool $success = true, array $details = [], ?string $agentName = null): bool
    {
        global $DB;
        $usersId = isset($_SESSION['glpiID']) ? (int)$_SESSION['glpiID'] : 0;
        return $DB->insert('glpi_plugin_glpiaiconnector_audits', [
            'users_id' => $usersId,
            'agent_name' => $agentName,
            'operation' => $operation,
            'itemtype' => $itemtype,
            'items_id' => $itemsId,
            'success' => $success ? 1 : 0,
            'details' => json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        ]);
    }
}
