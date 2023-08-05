Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var prompts_1 = require("app/actionCreators/prompts");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var appStoreConnectContext_1 = tslib_1.__importDefault(require("app/components/projects/appStoreConnectContext"));
var utils_1 = require("app/components/projects/appStoreConnectContext/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var APP_STORE_CONNECT_UPDATES = 'app_store_connect_updates';
function UpdateAlert(_a) {
    var api = _a.api, Wrapper = _a.Wrapper, isCompact = _a.isCompact, project = _a.project, organization = _a.organization, className = _a.className;
    var appStoreConnectContext = react_1.useContext(appStoreConnectContext_1.default);
    var _b = tslib_1.__read(react_1.useState(false), 2), isDismissed = _b[0], setIsDismissed = _b[1];
    react_1.useEffect(function () {
        checkPrompt();
    }, []);
    function checkPrompt() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var prompt;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!project ||
                            !appStoreConnectContext ||
                            !appStoreConnectContext.updateAlertMessage ||
                            isDismissed) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                organizationId: organization.id,
                                projectId: project.id,
                                feature: APP_STORE_CONNECT_UPDATES,
                            })];
                    case 1:
                        prompt = _a.sent();
                        setIsDismissed(promptIsDismissed_1.promptIsDismissed(prompt));
                        return [2 /*return*/];
                }
            });
        });
    }
    function handleDismiss() {
        if (!project) {
            return;
        }
        prompts_1.promptsUpdate(api, {
            organizationId: organization.id,
            projectId: project.id,
            feature: APP_STORE_CONNECT_UPDATES,
            status: 'dismissed',
        });
        setIsDismissed(true);
    }
    function renderMessage(appStoreConnectValidationData, projectSettingsLink) {
        if (!appStoreConnectValidationData.updateAlertMessage) {
            return null;
        }
        var updateAlertMessage = appStoreConnectValidationData.updateAlertMessage;
        return (<div>
        {updateAlertMessage}
        {isCompact && (<react_1.Fragment>
            &nbsp;
            <link_1.default to={updateAlertMessage ===
                    utils_1.appStoreConnectAlertMessage.appStoreCredentialsInvalid
                    ? projectSettingsLink
                    : projectSettingsLink + "&revalidateItunesSession=true"}>
              {updateAlertMessage ===
                    utils_1.appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt
                    ? locale_1.t('We recommend that you revalidate the session in the project settings')
                    : locale_1.t('Update it in the project settings to reconnect')}
            </link_1.default>
          </react_1.Fragment>)}
      </div>);
    }
    function renderActions(projectSettingsLink) {
        if (isCompact) {
            return (<ButtonClose priority="link" title={locale_1.t('Dismiss')} label={locale_1.t('Dismiss')} onClick={handleDismiss} icon={<icons_1.IconClose />}/>);
        }
        return (<Actions>
        <button_1.default priority="link" onClick={handleDismiss}>
          {locale_1.t('Dismiss')}
        </button_1.default>
        |
        <button_1.default priority="link" to={projectSettingsLink + "&revalidateItunesSession=true"}>
          {locale_1.t('Update session')}
        </button_1.default>
      </Actions>);
    }
    if (!project ||
        !appStoreConnectContext ||
        !appStoreConnectContext.updateAlertMessage ||
        isDismissed) {
        return null;
    }
    var projectSettingsLink = "/settings/" + organization.slug + "/projects/" + project.slug + "/debug-symbols/?customRepository=" + appStoreConnectContext.id;
    var notice = (<alert_1.default type="warning" icon={<icons_1.IconRefresh />} className={className}>
      <Content>
        {renderMessage(appStoreConnectContext, projectSettingsLink)}
        {renderActions(projectSettingsLink)}
      </Content>
    </alert_1.default>);
    return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
}
exports.default = withApi_1.default(UpdateAlert);
var Actions = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var Content = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ButtonClose = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=updateAlert.jsx.map