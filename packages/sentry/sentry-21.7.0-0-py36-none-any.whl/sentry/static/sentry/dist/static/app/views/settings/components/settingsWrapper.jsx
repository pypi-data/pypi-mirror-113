Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var scrollToTop_1 = tslib_1.__importDefault(require("app/views/settings/components/scrollToTop"));
var SettingsWrapper = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsWrapper, _super);
    function SettingsWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // save current context
        _this.state = {
            lastAppContext: _this.getLastAppContext(),
        };
        _this.handleShouldDisableScrollToTop = function (location, prevLocation) {
            var _a, _b;
            // we do not want to scroll to top when user just perform a search
            return (location.pathname === prevLocation.pathname &&
                ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) !== ((_b = prevLocation.query) === null || _b === void 0 ? void 0 : _b.query));
        };
        return _this;
    }
    SettingsWrapper.prototype.getChildContext = function () {
        return {
            lastAppContext: this.state.lastAppContext,
        };
    };
    SettingsWrapper.prototype.getLastAppContext = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        if (!!project) {
            return 'project';
        }
        if (!!organization) {
            return 'organization';
        }
        return null;
    };
    SettingsWrapper.prototype.render = function () {
        var _a = this.props, location = _a.location, children = _a.children;
        return (<StyledSettingsWrapper>
        <scrollToTop_1.default location={location} disable={this.handleShouldDisableScrollToTop}>
          {children}
        </scrollToTop_1.default>
      </StyledSettingsWrapper>);
    };
    SettingsWrapper.childContextTypes = {
        lastAppContext: prop_types_1.default.oneOf(['project', 'organization']),
    };
    return SettingsWrapper;
}(react_1.Component));
exports.default = withLatestContext_1.default(SettingsWrapper);
var StyledSettingsWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: -", "; /* to account for footer margin top */\n  line-height: 1;\n\n  .messages-container {\n    margin: 0;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: -", "; /* to account for footer margin top */\n  line-height: 1;\n\n  .messages-container {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.textColor; }, space_1.default(3));
var templateObject_1;
//# sourceMappingURL=settingsWrapper.jsx.map