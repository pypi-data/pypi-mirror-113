Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var functionName_1 = tslib_1.__importDefault(require("app/components/events/interfaces/frame/functionName"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ImageForBar = function (_a) {
    var frame = _a.frame, onShowAllImages = _a.onShowAllImages;
    var handleShowAllImages = function () {
        onShowAllImages('');
    };
    return (<Wrapper>
      <MatchedFunctionWrapper>
        <MatchedFunctionCaption>{locale_1.t('Image for: ')}</MatchedFunctionCaption>
        <functionName_1.default frame={frame}/>
      </MatchedFunctionWrapper>
      <ResetAddressFilterCaption onClick={handleShowAllImages}>
        {locale_1.t('Show all images')}
      </ResetAddressFilterCaption>
    </Wrapper>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n  justify-content: space-between;\n  padding: ", " ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  font-weight: 700;\n  code {\n    color: ", ";\n    font-size: ", ";\n    background: ", ";\n  }\n  a {\n    color: ", ";\n    &:hover {\n      text-decoration: underline;\n    }\n  }\n"], ["\n  display: flex;\n  align-items: baseline;\n  justify-content: space-between;\n  padding: ", " ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  font-weight: 700;\n  code {\n    color: ", ";\n    font-size: ", ";\n    background: ", ";\n  }\n  a {\n    color: ", ";\n    &:hover {\n      text-decoration: underline;\n    }\n  }\n"])), space_1.default(0.5), space_1.default(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.blue300; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.blue300; });
var MatchedFunctionWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n"], ["\n  display: flex;\n  align-items: baseline;\n"])));
var MatchedFunctionCaption = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  flex-shrink: 0;\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  flex-shrink: 0;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var ResetAddressFilterCaption = styled_1.default('a')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n  padding-left: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  color: ", " !important;\n  &:hover {\n    color: ", " !important;\n  }\n"], ["\n  display: flex;\n  flex-shrink: 0;\n  padding-left: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  color: ", " !important;\n  &:hover {\n    color: ", " !important;\n  }\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray300; });
exports.default = ImageForBar;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=imageForBar.jsx.map