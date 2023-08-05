Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function PaginationCaption(_a) {
    var caption = _a.caption;
    return <Wrapper>{caption}</Wrapper>;
}
exports.default = PaginationCaption;
var Wrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(2));
var templateObject_1;
//# sourceMappingURL=paginationCaption.jsx.map