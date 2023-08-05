Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var CommandLine = function (_a) {
    var children = _a.children;
    return <Wrapper>{children}</Wrapper>;
};
exports.default = CommandLine;
var Wrapper = styled_1.default('code')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n  font-family: ", ";\n  font-size: ", ";\n  white-space: nowrap;\n"], ["\n  padding: ", " ", ";\n  color: ", ";\n  background: ", ";\n  border: 1px solid ", ";\n  font-family: ", ";\n  font-size: ", ";\n  white-space: nowrap;\n"])), space_1.default(0.5), space_1.default(1), function (p) { return p.theme.pink300; }, function (p) { return p.theme.pink100; }, function (p) { return p.theme.pink200; }, function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1;
//# sourceMappingURL=commandLine.jsx.map