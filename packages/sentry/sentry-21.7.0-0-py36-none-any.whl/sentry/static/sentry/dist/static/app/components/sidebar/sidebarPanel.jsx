Object.defineProperty(exports, "__esModule", { value: true });
exports.getSidebarPanelContainer = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var animations_1 = require("app/styles/animations");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var PanelContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: fixed;\n  bottom: 0;\n  display: flex;\n  flex-direction: column;\n  z-index: ", ";\n  background: ", ";\n  color: ", ";\n  border-right: 1px solid ", ";\n  box-shadow: 1px 0 2px rgba(0, 0, 0, 0.06);\n  text-align: left;\n  animation: 200ms ", ";\n\n  ", ";\n"], ["\n  position: fixed;\n  bottom: 0;\n  display: flex;\n  flex-direction: column;\n  z-index: ", ";\n  background: ", ";\n  color: ", ";\n  border-right: 1px solid ", ";\n  box-shadow: 1px 0 2px rgba(0, 0, 0, 0.06);\n  text-align: left;\n  animation: 200ms ", ";\n\n  ", ";\n"])), function (p) { return p.theme.zIndex.sidebarPanel; }, function (p) { return p.theme.background; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.border; }, animations_1.slideInLeft, function (p) {
    return p.orientation === 'top'
        ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n          top: ", ";\n          left: 0;\n          right: 0;\n        "], ["\n          top: ", ";\n          left: 0;\n          right: 0;\n        "])), p.theme.sidebar.mobileHeight) : react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n          width: 360px;\n          top: 0;\n          left: ", ";\n        "], ["\n          width: 360px;\n          top: 0;\n          left: ", ";\n        "])), p.collapsed
        ? p.theme.sidebar.collapsedWidth
        : p.theme.sidebar.expandedWidth);
});
/**
 * Get the container element of the sidebar that react portals into.
 */
var getSidebarPanelContainer = function () {
    return document.getElementById('sidebar-flyout-portal');
};
exports.getSidebarPanelContainer = getSidebarPanelContainer;
var makePortal = function () {
    var portal = document.createElement('div');
    portal.setAttribute('id', 'sidebar-flyout-portal');
    document.body.appendChild(portal);
    return portal;
};
var SidebarPanel = /** @class */ (function (_super) {
    tslib_1.__extends(SidebarPanel, _super);
    function SidebarPanel(props) {
        var _this = _super.call(this, props) || this;
        _this.panelCloseHandler = function (evt) {
            if (!(evt.target instanceof Element)) {
                return;
            }
            var panel = exports.getSidebarPanelContainer();
            if (panel === null || panel === void 0 ? void 0 : panel.contains(evt.target)) {
                return;
            }
            _this.props.hidePanel();
        };
        _this.portalEl = exports.getSidebarPanelContainer() || makePortal();
        return _this;
    }
    SidebarPanel.prototype.componentDidMount = function () {
        document.addEventListener('click', this.panelCloseHandler);
    };
    SidebarPanel.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.panelCloseHandler);
    };
    SidebarPanel.prototype.render = function () {
        var _a = this.props, orientation = _a.orientation, collapsed = _a.collapsed, hidePanel = _a.hidePanel, title = _a.title, children = _a.children, props = tslib_1.__rest(_a, ["orientation", "collapsed", "hidePanel", "title", "children"]);
        var sidebar = (<PanelContainer collapsed={collapsed} orientation={orientation} {...props}>
        {title && (<SidebarPanelHeader>
            <Title>{title}</Title>
            <PanelClose onClick={hidePanel}/>
          </SidebarPanelHeader>)}
        <SidebarPanelBody hasHeader={!!title}>{children}</SidebarPanelBody>
      </PanelContainer>);
        return react_dom_1.default.createPortal(sidebar, this.portalEl);
    };
    return SidebarPanel;
}(React.Component));
exports.default = SidebarPanel;
var SidebarPanelHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  background: ", ";\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);\n  height: 60px;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-shrink: 1;\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  background: ", ";\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);\n  height: 60px;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-shrink: 1;\n"])), function (p) { return p.theme.border; }, space_1.default(3), function (p) { return p.theme.background; });
var SidebarPanelBody = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n  overflow: auto;\n  position: relative;\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n  overflow: auto;\n  position: relative;\n"])));
var PanelClose = styled_1.default(icons_1.IconClose)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n  position: relative;\n  padding: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  cursor: pointer;\n  position: relative;\n  padding: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, space_1.default(0.75), function (p) { return p.theme.textColor; });
PanelClose.defaultProps = {
    size: 'lg',
};
var Title = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: 0;\n"], ["\n  font-size: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=sidebarPanel.jsx.map