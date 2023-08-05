Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var IntegrationServerlessRow = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationServerlessRow, _super);
    function IntegrationServerlessRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            submitting: false,
        };
        _this.recordAction = function (action) {
            integrationUtil_1.trackIntegrationEvent('integrations.serverless_function_action', {
                integration: _this.props.integration.provider.key,
                integration_type: 'first_party',
                action: action,
            }, _this.props.organization);
        };
        _this.toggleEnable = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var serverlessFunction, action, data, resp, err_1;
            var _a, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        serverlessFunction = this.props.serverlessFunction;
                        action = this.enabled ? 'disable' : 'enable';
                        data = {
                            action: action,
                            target: serverlessFunction.name,
                        };
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        indicator_1.addLoadingMessage();
                        this.setState({ submitting: true });
                        // optimistically update enable state
                        this.props.onUpdateFunction({ enabled: !this.enabled });
                        this.recordAction(action);
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _c.sent();
                        // update remaining after response
                        this.props.onUpdateFunction(resp);
                        indicator_1.addSuccessMessage(locale_1.t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        // restore original on failure
                        this.props.onUpdateFunction(serverlessFunction);
                        indicator_1.addErrorMessage((_b = (_a = err_1.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : locale_1.t('Error occurred'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ submitting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.updateVersion = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var serverlessFunction, data, resp, err_2;
            var _a, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        serverlessFunction = this.props.serverlessFunction;
                        data = {
                            action: 'updateVersion',
                            target: serverlessFunction.name,
                        };
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        this.setState({ submitting: true });
                        // don't know the latest version but at least optimistically remove the update button
                        this.props.onUpdateFunction({ outOfDate: false });
                        indicator_1.addLoadingMessage();
                        this.recordAction('updateVersion');
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _c.sent();
                        // update remaining after response
                        this.props.onUpdateFunction(resp);
                        indicator_1.addSuccessMessage(locale_1.t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        // restore original on failure
                        this.props.onUpdateFunction(serverlessFunction);
                        indicator_1.addErrorMessage((_b = (_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : locale_1.t('Error occurred'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ submitting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Object.defineProperty(IntegrationServerlessRow.prototype, "enabled", {
        get: function () {
            return this.props.serverlessFunction.enabled;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationServerlessRow.prototype, "endpoint", {
        get: function () {
            var orgSlug = this.props.organization.slug;
            return "/organizations/" + orgSlug + "/integrations/" + this.props.integration.id + "/serverless-functions/";
        },
        enumerable: false,
        configurable: true
    });
    IntegrationServerlessRow.prototype.renderLayerStatus = function () {
        var serverlessFunction = this.props.serverlessFunction;
        if (!serverlessFunction.outOfDate) {
            return this.enabled ? locale_1.t('Latest') : locale_1.t('Disabled');
        }
        return (<UpdateButton size="small" priority="primary" onClick={this.updateVersion}>
        {locale_1.t('Update')}
      </UpdateButton>);
    };
    IntegrationServerlessRow.prototype.render = function () {
        var serverlessFunction = this.props.serverlessFunction;
        var version = serverlessFunction.version;
        // during optimistic update, we might be enabled without a version
        var versionText = this.enabled && version > 0 ? <react_1.Fragment>&nbsp;|&nbsp;v{version}</react_1.Fragment> : null;
        return (<Item>
        <NameWrapper>
          <NameRuntimeVersionWrapper>
            <Name>{serverlessFunction.name}</Name>
            <RuntimeAndVersion>
              <DetailWrapper>{serverlessFunction.runtime}</DetailWrapper>
              <DetailWrapper>{versionText}</DetailWrapper>
            </RuntimeAndVersion>
          </NameRuntimeVersionWrapper>
        </NameWrapper>
        <LayerStatusWrapper>{this.renderLayerStatus()}</LayerStatusWrapper>
        <StyledSwitch isActive={this.enabled} isDisabled={this.state.submitting} size="sm" toggle={this.toggleEnable}/>
      </Item>);
    };
    return IntegrationServerlessRow;
}(react_1.Component));
exports.default = withApi_1.default(IntegrationServerlessRow);
var Item = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"], ["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; }, space_1.default(1));
var ItemWrapper = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 32px;\n  vertical-align: middle;\n  display: flex;\n  align-items: center;\n"], ["\n  height: 32px;\n  vertical-align: middle;\n  display: flex;\n  align-items: center;\n"])));
var NameWrapper = styled_1.default(ItemWrapper)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-area: function-name;\n"], ["\n  grid-area: function-name;\n"])));
var LayerStatusWrapper = styled_1.default(ItemWrapper)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-area: layer-status;\n"], ["\n  grid-area: layer-status;\n"])));
var StyledSwitch = styled_1.default(switchButton_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-area: enable-switch;\n"], ["\n  grid-area: enable-switch;\n"])));
var UpdateButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject([""], [""])));
var NameRuntimeVersionWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Name = styled_1.default("span")(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space_1.default(1));
var RuntimeAndVersion = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var DetailWrapper = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  line-height: 1.2;\n"], ["\n  line-height: 1.2;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=integrationServerlessRow.jsx.map