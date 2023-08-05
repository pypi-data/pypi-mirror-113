Object.defineProperty(exports, "__esModule", { value: true });
exports.PluginConfig = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var plugins_1 = tslib_1.__importDefault(require("app/plugins"));
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var PluginConfig = /** @class */ (function (_super) {
    tslib_1.__extends(PluginConfig, _super);
    function PluginConfig() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: !plugins_1.default.isLoaded(_this.props.data),
            testResults: '',
        };
        _this.handleDisablePlugin = function () {
            _this.props.onDisablePlugin(_this.props.data);
        };
        _this.handleTestPlugin = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ testResults: '' });
                        indicator_1.addLoadingMessage(locale_1.t('Sending test...'));
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(this.getPluginEndpoint(), {
                                method: 'POST',
                                data: {
                                    test: true,
                                },
                            })];
                    case 2:
                        data = _a.sent();
                        this.setState({ testResults: JSON.stringify(data.detail) });
                        indicator_1.addSuccessMessage(locale_1.t('Test Complete!'));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('An unexpected error occurred while testing your plugin. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    PluginConfig.prototype.componentDidMount = function () {
        this.loadPlugin(this.props.data);
    };
    PluginConfig.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        this.loadPlugin(nextProps.data);
    };
    PluginConfig.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return !isEqual_1.default(nextState, this.state) || !isEqual_1.default(nextProps.data, this.props.data);
    };
    PluginConfig.prototype.loadPlugin = function (data) {
        var _this = this;
        this.setState({
            loading: true,
        }, function () {
            plugins_1.default.load(data, function () {
                _this.setState({ loading: false });
            });
        });
    };
    PluginConfig.prototype.getPluginEndpoint = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, data = _a.data;
        return "/projects/" + organization.slug + "/" + project.slug + "/plugins/" + data.id + "/";
    };
    PluginConfig.prototype.createMarkup = function () {
        return { __html: this.props.data.doc };
    };
    PluginConfig.prototype.render = function () {
        var data = this.props.data;
        // If passed via props, use that value instead of from `data`
        var enabled = typeof this.props.enabled !== 'undefined' ? this.props.enabled : data.enabled;
        return (<panels_1.Panel className={"plugin-config ref-plugin-config-" + data.id} data-test-id="plugin-config">
        <panels_1.PanelHeader hasButtons>
          <PluginName>
            <StyledPluginIcon pluginId={data.id}/>
            <span>{data.name}</span>
          </PluginName>

          {data.canDisable && enabled && (<Actions>
              {data.isTestable && (<TestPluginButton onClick={this.handleTestPlugin} size="small">
                  {locale_1.t('Test Plugin')}
                </TestPluginButton>)}
              <button_1.default size="small" onClick={this.handleDisablePlugin}>
                {locale_1.t('Disable')}
              </button_1.default>
            </Actions>)}
        </panels_1.PanelHeader>

        {data.status === 'beta' && (<panels_1.PanelAlert type="warning">
            {locale_1.t('This plugin is considered beta and may change in the future.')}
          </panels_1.PanelAlert>)}

        {this.state.testResults !== '' && (<panels_1.PanelAlert type="info">
            <strong>Test Results</strong>
            <div>{this.state.testResults}</div>
          </panels_1.PanelAlert>)}

        <StyledPanelBody>
          <div dangerouslySetInnerHTML={this.createMarkup()}/>
          {this.state.loading ? (<loadingIndicator_1.default />) : (plugins_1.default.get(data).renderSettings({
                organization: this.props.organization,
                project: this.props.project,
            }))}
        </StyledPanelBody>
      </panels_1.Panel>);
    };
    PluginConfig.defaultProps = {
        onDisablePlugin: function () { },
    };
    return PluginConfig;
}(react_1.Component));
exports.PluginConfig = PluginConfig;
exports.default = withApi_1.default(PluginConfig);
var PluginName = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n"])));
var StyledPluginIcon = styled_1.default(pluginIcon_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var Actions = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var TestPluginButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  padding-bottom: 0;\n"], ["\n  padding: ", ";\n  padding-bottom: 0;\n"])), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=pluginConfig.jsx.map