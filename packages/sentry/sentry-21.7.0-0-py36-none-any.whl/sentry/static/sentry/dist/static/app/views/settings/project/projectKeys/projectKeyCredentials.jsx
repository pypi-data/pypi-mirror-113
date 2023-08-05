Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var DEFAULT_PROPS = {
    showDsn: true,
    showDsnPublic: true,
    showSecurityEndpoint: true,
    showMinidump: true,
    showUnreal: true,
    showPublicKey: false,
    showSecretKey: false,
    showProjectId: false,
};
var ProjectKeyCredentials = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectKeyCredentials, _super);
    function ProjectKeyCredentials() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDeprecatedDsn: false,
        };
        _this.toggleDeprecatedDsn = function () {
            _this.setState(function (state) { return ({
                showDeprecatedDsn: !state.showDeprecatedDsn,
            }); });
        };
        return _this;
    }
    ProjectKeyCredentials.prototype.render = function () {
        var showDeprecatedDsn = this.state.showDeprecatedDsn;
        var _a = this.props, projectId = _a.projectId, data = _a.data, showDsn = _a.showDsn, showDsnPublic = _a.showDsnPublic, showSecurityEndpoint = _a.showSecurityEndpoint, showMinidump = _a.showMinidump, showUnreal = _a.showUnreal, showPublicKey = _a.showPublicKey, showSecretKey = _a.showSecretKey, showProjectId = _a.showProjectId;
        return (<react_1.Fragment>
        {showDsnPublic && (<field_1.default label={locale_1.t('DSN')} inline={false} flexibleControlStateSize help={locale_1.tct('The DSN tells the SDK where to send the events to. [link]', {
                    link: showDsn ? (<link_1.default to="" onClick={this.toggleDeprecatedDsn}>
                  {showDeprecatedDsn
                            ? locale_1.t('Hide deprecated DSN')
                            : locale_1.t('Show deprecated DSN')}
                </link_1.default>) : null,
                })}>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.dsn.public,
                    fixed: '__DSN__',
                })}
            </textCopyInput_1.default>
            {showDeprecatedDsn && (<StyledField label={null} help={locale_1.t('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
                <textCopyInput_1.default>
                  {getDynamicText_1.default({
                        value: data.dsn.secret,
                        fixed: '__DSN_DEPRECATED__',
                    })}
                </textCopyInput_1.default>
              </StyledField>)}
          </field_1.default>)}

        {/* this edge case should imho not happen, but just to be sure */}
        {!showDsnPublic && showDsn && (<field_1.default label={locale_1.t('DSN (Deprecated)')} help={locale_1.t('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.dsn.secret,
                    fixed: '__DSN_DEPRECATED__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showSecurityEndpoint && (<field_1.default label={locale_1.t('Security Header Endpoint')} help={locale_1.t('Use your security header endpoint for features like CSP and Expect-CT reports.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.dsn.security,
                    fixed: '__SECURITY_HEADER_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showMinidump && (<field_1.default label={locale_1.t('Minidump Endpoint')} help={locale_1.tct('Use this endpoint to upload [link], for example with Electron, Crashpad or Breakpad.', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/guides/minidumps/">
                    minidump crash reports
                  </externalLink_1.default>),
                })} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.dsn.minidump,
                    fixed: '__MINIDUMP_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showUnreal && (<field_1.default label={locale_1.t('Unreal Engine 4 Endpoint')} help={locale_1.t('Use this endpoint to configure your UE4 Crash Reporter.')} inline={false} flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.dsn.unreal || '',
                    fixed: '__UNREAL_ENDPOINT__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showPublicKey && (<field_1.default label={locale_1.t('Public Key')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.public,
                    fixed: '__PUBLICKEY__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showSecretKey && (<field_1.default label={locale_1.t('Secret Key')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: data.secret,
                    fixed: '__SECRETKEY__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}

        {showProjectId && (<field_1.default label={locale_1.t('Project ID')} inline flexibleControlStateSize>
            <textCopyInput_1.default>
              {getDynamicText_1.default({
                    value: projectId,
                    fixed: '__PROJECTID__',
                })}
            </textCopyInput_1.default>
          </field_1.default>)}
      </react_1.Fragment>);
    };
    ProjectKeyCredentials.defaultProps = DEFAULT_PROPS;
    return ProjectKeyCredentials;
}(react_1.Component));
var StyledField = styled_1.default(field_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " 0 0 0;\n"], ["\n  padding: ", " 0 0 0;\n"])), space_1.default(0.5));
exports.default = ProjectKeyCredentials;
var templateObject_1;
//# sourceMappingURL=projectKeyCredentials.jsx.map