Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var CrashTitle = function (_a) {
    var title = _a.title, newestFirst = _a.newestFirst, beforeTitle = _a.beforeTitle, _b = _a.hideGuide, hideGuide = _b === void 0 ? false : _b, onChange = _a.onChange;
    var handleToggleOrder = function () {
        if (onChange) {
            onChange({ newestFirst: !newestFirst });
        }
    };
    return (<Wrapper>
      {beforeTitle}
      <StyledH3>
        <guideAnchor_1.default target="exception" disabled={hideGuide} position="bottom">
          {title}
        </guideAnchor_1.default>
        {onChange && (<tooltip_1.default title={locale_1.t('Toggle stack trace order')}>
            <small>
              (
              <span onClick={handleToggleOrder}>
                {newestFirst ? locale_1.t('most recent call first') : locale_1.t('most recent call last')}
              </span>
              )
            </small>
          </tooltip_1.default>)}
      </StyledH3>
    </Wrapper>);
};
exports.default = CrashTitle;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-wrap: wrap;\n  flex-grow: 1;\n  justify-content: flex-start;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-wrap: wrap;\n  flex-grow: 1;\n  justify-content: flex-start;\n"])));
var StyledH3 = styled_1.default('h3')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  max-width: 100%;\n  white-space: nowrap;\n"], ["\n  margin-bottom: 0;\n  max-width: 100%;\n  white-space: nowrap;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=crashTitle.jsx.map