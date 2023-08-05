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
var ProjectHpkpReports = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectHpkpReports, _super);
    function ProjectHpkpReports() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectHpkpReports.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectHpkpReports.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('HTTP Public Key Pinning (HPKP)'), projectId, false);
    };
    ProjectHpkpReports.prototype.getInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            ("        'report-uri=\"" + reportUri_1.getSecurityDsn(keyList) + "\"' \n") +
            '    return response\n');
    };
    ProjectHpkpReports.prototype.getReportOnlyInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins-Report-Only'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            ("        'report-uri=\"" + reportUri_1.getSecurityDsn(keyList) + "\"' \n") +
            '    return response\n');
    };
    ProjectHpkpReports.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (!keyList) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('HTTP Public Key Pinning')}/>

        <previewFeature_1.default />

        <reportUri_1.default keyList={keyList} orgId={params.orgId} projectId={params.projectId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('About')}</panels_1.PanelHeader>

          <panels_1.PanelBody withPadding>
            <p>
              {locale_1.tct("[link:HTTP Public Key Pinning]\n              (HPKP) is a security feature that tells a web client to associate a specific\n              cryptographic public key with a certain web server to decrease the risk of MITM\n              attacks with forged certificates. It's enforced by browser vendors, and Sentry\n              supports capturing violations using the standard reporting hooks.", {
                link: (<externalLink_1.default href="https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning"/>),
            })}
            </p>

            <p>
              {locale_1.t("To configure HPKP reports\n              in Sentry, you'll need to send a header from your server describing your\n              policy, as well specifying the authenticated Sentry endpoint.")}
            </p>

            <p>
              {locale_1.t('For example, in Python you might achieve this via a simple web middleware')}
            </p>
            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {locale_1.t("Alternatively you can setup HPKP reports to simply send reports rather than\n              actually enforcing the policy")}
            </p>
            <pre>{this.getReportOnlyInstructions(keyList)}</pre>

            <p>
              {locale_1.tct("We recommend setting this up to only run on a percentage of requests, as\n              otherwise you may find that you've quickly exhausted your quota. For more\n              information, take a look at [link:the documentation on MDN].", {
                link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning"/>),
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return ProjectHpkpReports;
}(asyncView_1.default));
exports.default = ProjectHpkpReports;
//# sourceMappingURL=hpkp.jsx.map