Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var linkWithConfirmation_1 = tslib_1.__importDefault(require("app/components/links/linkWithConfirmation"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
function OrganizationApiKeysList(_a) {
    var params = _a.params, routes = _a.routes, keys = _a.keys, busy = _a.busy, loading = _a.loading, onAddApiKey = _a.onAddApiKey, onRemove = _a.onRemove;
    var hasKeys = keys && keys.length;
    var action = (<button_1.default priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} busy={busy} disabled={busy} onClick={onAddApiKey}>
      {locale_1.t('New API Key')}
    </button_1.default>);
    return (<div>
      <settingsPageHeader_1.default title={locale_1.t('API Keys')} action={action}/>

      <textBlock_1.default>
        {locale_1.tct("API keys grant access to the [api:developer web API].\n          If you're looking to configure a Sentry client, you'll need a\n          client key which is available in your project settings.", {
            api: <externalLink_1.default href="https://docs.sentry.io/api/"/>,
        })}
      </textBlock_1.default>

      <alertLink_1.default to="/settings/account/api/auth-tokens/" priority="info">
        {locale_1.tct('Until Sentry supports OAuth, you might want to switch to using [tokens:Auth Tokens] instead.', {
            tokens: <u />,
        })}
      </alertLink_1.default>

      <panels_1.PanelTable isLoading={loading} isEmpty={!hasKeys} emptyMessage={locale_1.t('No API keys for this organization')} headers={[locale_1.t('Name'), locale_1.t('Key'), locale_1.t('Actions')]}>
        {keys &&
            keys.map(function (_a) {
                var id = _a.id, key = _a.key, label = _a.label;
                var apiDetailsUrl = recreateRoute_1.default(id + "/", {
                    params: params,
                    routes: routes,
                });
                return (<react_1.Fragment key={key}>
                <Cell>
                  <link_1.default to={apiDetailsUrl}>{label}</link_1.default>
                </Cell>

                <div>
                  <AutoSelectTextInput readOnly>{key}</AutoSelectTextInput>
                </div>

                <Cell>
                  <linkWithConfirmation_1.default aria-label={locale_1.t('Remove API Key')} className="btn btn-default btn-sm" onConfirm={function () { return onRemove(id); }} message={locale_1.t('Are you sure you want to remove this API key?')} title={locale_1.t('Remove API Key?')}>
                    <icons_1.IconDelete size="xs" css={{ position: 'relative', top: '2px' }}/>
                  </linkWithConfirmation_1.default>
                </Cell>
              </react_1.Fragment>);
            })}
      </panels_1.PanelTable>
    </div>);
}
var Cell = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var AutoSelectTextInput = styled_1.default(autoSelectText_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return input_1.inputStyles(p); });
exports.default = OrganizationApiKeysList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=organizationApiKeysList.jsx.map