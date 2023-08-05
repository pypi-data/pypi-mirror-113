Object.defineProperty(exports, "__esModule", { value: true });
exports.InstalledPlugin = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var InstalledPlugin = /** @class */ (function (_super) {
    tslib_1.__extends(InstalledPlugin, _super);
    function InstalledPlugin() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pluginUpdate = function (data, method) {
            if (method === void 0) { method = 'POST'; }
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _a, organization, projectItem, plugin;
                return tslib_1.__generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.props, organization = _a.organization, projectItem = _a.projectItem, plugin = _a.plugin;
                            // no try/catch so the caller will have to have it
                            return [4 /*yield*/, this.props.api.requestPromise("/projects/" + organization.slug + "/" + projectItem.projectSlug + "/plugins/" + plugin.id + "/", {
                                    method: method,
                                    data: data,
                                })];
                        case 1:
                            // no try/catch so the caller will have to have it
                            _b.sent();
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.updatePluginEnableStatus = function (enabled) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!enabled) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.pluginUpdate({ enabled: enabled })];
                    case 1:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, this.pluginUpdate({}, 'DELETE')];
                    case 3:
                        _a.sent();
                        _a.label = 4;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleReset = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        indicator_1.addLoadingMessage(locale_1.t('Removing...'));
                        return [4 /*yield*/, this.pluginUpdate({ reset: true })];
                    case 1:
                        _a.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Configuration was removed'));
                        this.props.onResetConfiguration(this.projectId);
                        this.props.trackIntegrationEvent('integrations.uninstall_completed');
                        return [3 /*break*/, 3];
                    case 2:
                        _err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to remove configuration'));
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.handleUninstallClick = function () {
            _this.props.trackIntegrationEvent('integrations.uninstall_clicked');
        };
        _this.toggleEnablePlugin = function (projectId, status) {
            if (status === void 0) { status = true; }
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _err_2;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            indicator_1.addLoadingMessage(locale_1.t('Enabling...'));
                            return [4 /*yield*/, this.updatePluginEnableStatus(status)];
                        case 1:
                            _a.sent();
                            indicator_1.addSuccessMessage(status ? locale_1.t('Configuration was enabled.') : locale_1.t('Configuration was disabled.'));
                            this.props.onPluginEnableStatusChange(projectId, status);
                            this.props.trackIntegrationEvent(status ? 'integrations.enabled' : 'integrations.disabled');
                            return [3 /*break*/, 3];
                        case 2:
                            _err_2 = _a.sent();
                            indicator_1.addErrorMessage(status
                                ? locale_1.t('Unable to enable configuration.')
                                : locale_1.t('Unable to disable configuration.'));
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    Object.defineProperty(InstalledPlugin.prototype, "projectId", {
        get: function () {
            return this.props.projectItem.projectId;
        },
        enumerable: false,
        configurable: true
    });
    InstalledPlugin.prototype.getConfirmMessage = function () {
        return (<react_1.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.t('Deleting this installation will disable the integration for this project and remove any configurations.')}
        </alert_1.default>
      </react_1.Fragment>);
    };
    Object.defineProperty(InstalledPlugin.prototype, "projectForBadge", {
        get: function () {
            // this function returns the project as needed for the ProjectBadge component
            var projectItem = this.props.projectItem;
            return {
                slug: projectItem.projectSlug,
                platform: projectItem.projectPlatform ? projectItem.projectPlatform : undefined,
            };
        },
        enumerable: false,
        configurable: true
    });
    InstalledPlugin.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, plugin = _a.plugin, organization = _a.organization, projectItem = _a.projectItem;
        return (<Container>
        <access_1.default access={['org:integrations']}>
          {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<IntegrationFlex className={className}>
              <IntegrationItemBox>
                <projectBadge_1.default project={_this.projectForBadge}/>
              </IntegrationItemBox>
              <div>
                {<StyledButton borderless icon={<icons_1.IconSettings />} disabled={!hasAccess} to={"/settings/" + organization.slug + "/projects/" + projectItem.projectSlug + "/plugins/" + plugin.id + "/"} data-test-id="integration-configure-button">
                    {locale_1.t('Configure')}
                  </StyledButton>}
              </div>
              <div>
                <confirm_1.default priority="danger" onConfirming={_this.handleUninstallClick} disabled={!hasAccess} confirmText="Delete Installation" onConfirm={function () { return _this.handleReset(); }} message={_this.getConfirmMessage()}>
                  <StyledButton disabled={!hasAccess} borderless icon={<icons_1.IconDelete />} data-test-id="integration-remove-button">
                    {locale_1.t('Uninstall')}
                  </StyledButton>
                </confirm_1.default>
              </div>
              <switchButton_1.default isActive={projectItem.enabled} toggle={function () {
                        return _this.toggleEnablePlugin(projectItem.projectId, !projectItem.enabled);
                    }} isDisabled={!hasAccess}/>
            </IntegrationFlex>);
            }}
        </access_1.default>
      </Container>);
    };
    return InstalledPlugin;
}(react_1.Component));
exports.InstalledPlugin = InstalledPlugin;
exports.default = withApi_1.default(InstalledPlugin);
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; });
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var IntegrationFlex = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationItemBox = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: row;\n  min-width: 0;\n"], ["\n  flex: 1;\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: row;\n  min-width: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=installedPlugin.jsx.map