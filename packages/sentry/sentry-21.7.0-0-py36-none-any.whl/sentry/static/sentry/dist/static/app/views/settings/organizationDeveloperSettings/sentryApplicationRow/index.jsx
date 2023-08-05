Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var sentryAppPublishRequestModal_1 = tslib_1.__importDefault(require("app/components/modals/sentryAppPublishRequestModal"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var sentryApplicationRowButtons_1 = tslib_1.__importDefault(require("./sentryApplicationRowButtons"));
var SentryApplicationRow = /** @class */ (function (_super) {
    tslib_1.__extends(SentryApplicationRow, _super);
    function SentryApplicationRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handlePublish = function () {
            var app = _this.props.app;
            modal_1.openModal(function (deps) { return <sentryAppPublishRequestModal_1.default app={app} {...deps}/>; });
        };
        return _this;
    }
    Object.defineProperty(SentryApplicationRow.prototype, "isInternal", {
        get: function () {
            return this.props.app.status === 'internal';
        },
        enumerable: false,
        configurable: true
    });
    SentryApplicationRow.prototype.hideStatus = function () {
        // no publishing for internal apps so hide the status on the developer settings page
        return this.isInternal;
    };
    SentryApplicationRow.prototype.renderStatus = function () {
        var app = this.props.app;
        if (this.hideStatus()) {
            return null;
        }
        return <PublishStatus status={app.status}/>;
    };
    SentryApplicationRow.prototype.render = function () {
        var _a = this.props, app = _a.app, organization = _a.organization, onRemoveApp = _a.onRemoveApp;
        return (<SentryAppItem data-test-id={app.slug}>
        <StyledFlex>
          <pluginIcon_1.default size={36} pluginId={app.slug}/>
          <SentryAppBox>
            <SentryAppName hideStatus={this.hideStatus()}>
              <react_router_1.Link to={"/settings/" + organization.slug + "/developer-settings/" + app.slug + "/"}>
                {app.name}
              </react_router_1.Link>
            </SentryAppName>
            <SentryAppDetails>{this.renderStatus()}</SentryAppDetails>
          </SentryAppBox>

          <Box>
            <sentryApplicationRowButtons_1.default organization={organization} app={app} onClickRemove={onRemoveApp} onClickPublish={this.handlePublish}/>
          </Box>
        </StyledFlex>
      </SentryAppItem>);
    };
    return SentryApplicationRow;
}(react_1.PureComponent));
exports.default = SentryApplicationRow;
var Flex = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Box = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject([""], [""])));
var SentryAppItem = styled_1.default(panels_1.PanelItem)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n  padding: 5px;\n"], ["\n  flex-direction: column;\n  padding: 5px;\n"])));
var StyledFlex = styled_1.default(Flex)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n  padding: 10px;\n"], ["\n  justify-content: center;\n  padding: 10px;\n"])));
var SentryAppBox = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding-left: 15px;\n  padding-right: 15px;\n  flex: 1;\n"], ["\n  padding-left: 15px;\n  padding-right: 15px;\n  flex: 1;\n"])));
var SentryAppDetails = styled_1.default(Flex)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"], ["\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"])));
var SentryAppName = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), function (p) { return (p.hideStatus ? '10px' : '0px'); });
var CenterFlex = styled_1.default(Flex)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var PublishStatus = styled_1.default(function (_a) {
    var status = _a.status, props = tslib_1.__rest(_a, ["status"]);
    return (<CenterFlex>
    <div {...props}>{locale_1.t("" + status)}</div>
  </CenterFlex>);
})(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"])), function (props) {
    return props.status === 'published' ? props.theme.success : props.theme.gray300;
}, space_1.default(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=index.jsx.map