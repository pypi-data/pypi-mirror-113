Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panel_1 = tslib_1.__importDefault(require("app/components/panels/panel"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var BODY_CLASSES = ['narrow'];
var Layout = /** @class */ (function (_super) {
    tslib_1.__extends(Layout, _super);
    function Layout() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Layout.prototype.componentDidMount = function () {
        var _a;
        (_a = document.body.classList).add.apply(_a, tslib_1.__spreadArray([], tslib_1.__read(BODY_CLASSES)));
    };
    Layout.prototype.componentWillUnmount = function () {
        var _a;
        (_a = document.body.classList).remove.apply(_a, tslib_1.__spreadArray([], tslib_1.__read(BODY_CLASSES)));
    };
    Layout.prototype.render = function () {
        var children = this.props.children;
        return (<div className="app">
        <AuthContainer>
          <div className="pattern-bg"/>
          <AuthPanel>
            <AuthSidebar>
              <SentryButton />
            </AuthSidebar>
            <div>{children}</div>
          </AuthPanel>
        </AuthContainer>
      </div>);
    };
    return Layout;
}(React.Component));
var AuthContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  justify-content: center;\n  padding-top: 5vh;\n"], ["\n  display: flex;\n  align-items: flex-start;\n  justify-content: center;\n  padding-top: 5vh;\n"])));
var AuthPanel = styled_1.default(panel_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  min-width: 550px;\n  display: inline-grid;\n  grid-template-columns: 60px 1fr;\n"], ["\n  min-width: 550px;\n  display: inline-grid;\n  grid-template-columns: 60px 1fr;\n"])));
var AuthSidebar = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  padding: ", ";\n  border-radius: ", " 0 0 ", ";\n  margin: -1px;\n  margin-right: 0;\n  background: #564f64;\n  background-image: linear-gradient(\n    -180deg,\n    rgba(52, 44, 62, 0) 0%,\n    rgba(52, 44, 62, 0.5) 100%\n  );\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  padding: ", ";\n  border-radius: ", " 0 0 ", ";\n  margin: -1px;\n  margin-right: 0;\n  background: #564f64;\n  background-image: linear-gradient(\n    -180deg,\n    rgba(52, 44, 62, 0) 0%,\n    rgba(52, 44, 62, 0.5) 100%\n  );\n"])), space_1.default(3), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var SentryButton = styled_1.default(function (p) { return (<link_1.default to="/" {...p}>
      <icons_1.IconSentry size="24px"/>
    </link_1.default>); })(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: #fff;\n\n  &:hover,\n  &:focus {\n    color: #fff;\n  }\n"], ["\n  color: #fff;\n\n  &:hover,\n  &:focus {\n    color: #fff;\n  }\n"])));
exports.default = Layout;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=layout.jsx.map