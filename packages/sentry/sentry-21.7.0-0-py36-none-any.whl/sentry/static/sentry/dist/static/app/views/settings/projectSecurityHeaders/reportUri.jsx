Object.defineProperty(exports, "__esModule", { value: true });
exports.getSecurityDsn = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var DEFAULT_ENDPOINT = 'https://sentry.example.com/api/security-report/';
function getSecurityDsn(keyList) {
    var endpoint = keyList.length ? keyList[0].dsn.security : DEFAULT_ENDPOINT;
    return getDynamicText_1.default({
        value: endpoint,
        fixed: DEFAULT_ENDPOINT,
    });
}
exports.getSecurityDsn = getSecurityDsn;
function ReportUri(_a) {
    var keyList = _a.keyList, orgId = _a.orgId, projectId = _a.projectId;
    return (<panels_1.Panel>
      <panels_1.PanelHeader>{locale_1.t('Report URI')}</panels_1.PanelHeader>
      <panels_1.PanelBody>
        <panels_1.PanelAlert type="info">
          {locale_1.tct("We've automatically pulled these credentials from your available [link:Client Keys]", {
            link: <react_router_1.Link to={"/settings/" + orgId + "/projects/" + projectId + "/keys/"}/>,
        })}
        </panels_1.PanelAlert>
        <field_1.default inline={false} flexibleControlStateSize>
          <textCopyInput_1.default>{getSecurityDsn(keyList)}</textCopyInput_1.default>
        </field_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = ReportUri;
//# sourceMappingURL=reportUri.jsx.map