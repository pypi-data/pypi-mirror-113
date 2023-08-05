Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../utils");
function Browser(_a) {
    var browser = _a.browser, isEnabled = _a.isEnabled, onToggle = _a.onToggle;
    var _b = utils_1.LEGACY_BROWSER_LIST[browser], icon = _b.icon, title = _b.title;
    return (<react_1.Fragment>
      <BrowserWrapper>
        <Icon className={"icon-" + icon}/>
        {title}
      </BrowserWrapper>
      <SwitchWrapper>
        <switchButton_1.default size="lg" isActive={isEnabled} toggle={onToggle}/>
      </SwitchWrapper>
    </react_1.Fragment>);
}
exports.default = Browser;
var BrowserWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeLarge; });
var Icon = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 24px;\n  height: 24px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 24px 24px;\n  flex-shrink: 0;\n"], ["\n  width: 24px;\n  height: 24px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 24px 24px;\n  flex-shrink: 0;\n"])));
var SwitchWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=browser.jsx.map