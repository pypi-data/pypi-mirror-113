Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var reportUri_1 = tslib_1.__importDefault(require("app/views/settings/projectSecurityHeaders/reportUri"));
var ProjectSecurityHeaders = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectSecurityHeaders, _super);
    function ProjectSecurityHeaders() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectSecurityHeaders.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectSecurityHeaders.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Security Headers'), projectId, false);
    };
    ProjectSecurityHeaders.prototype.getReports = function () {
        return [
            {
                name: 'Content Security Policy (CSP)',
                url: recreateRoute_1.default('csp/', this.props),
            },
            {
                name: 'Certificate Transparency (Expect-CT)',
                url: recreateRoute_1.default('expect-ct/', this.props),
            },
            {
                name: 'HTTP Public Key Pinning (HPKP)',
                url: recreateRoute_1.default('hpkp/', this.props),
            },
        ];
    };
    ProjectSecurityHeaders.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (keyList === null) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Security Header Reports')}/>

        <reportUri_1.default keyList={keyList} projectId={params.projectId} orgId={params.orgId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Additional Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <textBlock_1.default style={{ marginBottom: 20 }}>
              {locale_1.tct('In addition to the [key_param] parameter, you may also pass the following within the querystring for the report URI:', {
                key_param: <code>sentry_key</code>,
            })}
            </textBlock_1.default>
            <table className="table" style={{ marginBottom: 0 }}>
              <tbody>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_environment</th>
                  <td style={{ padding: '8px 5px' }}>
                    {locale_1.t('The environment name (e.g. production)')}.
                  </td>
                </tr>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_release</th>
                  <td style={{ padding: '8px 5px' }}>
                    {locale_1.t('The version of the application.')}
                  </td>
                </tr>
              </tbody>
            </table>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Supported Formats')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {this.getReports().map(function (_a) {
                var name = _a.name, url = _a.url;
                return (<ReportItem key={url}>
                <HeaderName>{name}</HeaderName>
                <button_1.default to={url} priority="primary">
                  {locale_1.t('Instructions')}
                </button_1.default>
              </ReportItem>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ProjectSecurityHeaders;
}(asyncView_1.default));
exports.default = ProjectSecurityHeaders;
var ReportItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
var HeaderName = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map