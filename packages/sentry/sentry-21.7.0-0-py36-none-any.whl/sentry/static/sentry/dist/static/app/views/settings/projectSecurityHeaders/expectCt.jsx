Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var previewFeature_1 = tslib_1.__importDefault(require("app/components/previewFeature"));
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var reportUri_1 = tslib_1.__importStar(require("app/views/settings/projectSecurityHeaders/reportUri"));
var ProjectExpectCtReports = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectExpectCtReports, _super);
    function ProjectExpectCtReports() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectExpectCtReports.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectExpectCtReports.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Certificate Transparency (Expect-CT)'), projectId, false);
    };
    ProjectExpectCtReports.prototype.getInstructions = function (keyList) {
        return "Expect-CT: report-uri=\"" + reportUri_1.getSecurityDsn(keyList) + "\"";
    };
    ProjectExpectCtReports.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (!keyList) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Certificate Transparency')}/>

        <previewFeature_1.default />

        <reportUri_1.default keyList={keyList} orgId={params.orgId} projectId={params.orgId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{'About'}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {locale_1.tct("[link:Certificate Transparency]\n      (CT) is a security standard which helps track and identify valid certificates, allowing identification of maliciously issued certificates", {
                link: (<externalLink_1.default href="https://en.wikipedia.org/wiki/Certificate_Transparency"/>),
            })}
            </p>
            <p>
              {locale_1.tct("To configure reports in Sentry, you'll need to configure the [header] a header from your server:", {
                header: <code>Expect-CT</code>,
            })}
            </p>

            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {locale_1.tct('For more information, see [link:the article on MDN].', {
                link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT"/>),
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ProjectExpectCtReports;
}(asyncView_1.default));
exports.default = ProjectExpectCtReports;
//# sourceMappingURL=expectCt.jsx.map