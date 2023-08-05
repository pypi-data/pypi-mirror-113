Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var ShortId = function (_a) {
    var shortId = _a.shortId, avatar = _a.avatar;
    return (<Wrapper>
    <AvatarWrapper>{avatar}</AvatarWrapper>
    <IdWrapper>{shortId}</IdWrapper>
  </Wrapper>);
};
exports.default = ShortId;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraSmall; });
var AvatarWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: 3px;\n  flex-shrink: 0;\n"], ["\n  margin-right: 3px;\n  flex-shrink: 0;\n"])));
var IdWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  margin-top: 1px;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  margin-top: 1px;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=shortId.jsx.map