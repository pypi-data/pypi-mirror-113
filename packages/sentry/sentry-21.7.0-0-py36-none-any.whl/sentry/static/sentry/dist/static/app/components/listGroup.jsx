Object.defineProperty(exports, "__esModule", { value: true });
exports.ListGroupItem = exports.ListGroup = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ListGroupItem = styled_1.default('li')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: block;\n  min-height: 36px;\n  border: 1px solid ", ";\n\n  padding: ", " ", ";\n\n  margin-bottom: -1px;\n  ", "\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    border-top-right-radius: ", ";\n  }\n  &:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"], ["\n  position: relative;\n  display: block;\n  min-height: 36px;\n  border: 1px solid ", ";\n\n  padding: ", " ", ";\n\n  margin-bottom: -1px;\n  ", "\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    border-top-right-radius: ", ";\n  }\n  &:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"])), function (p) { return p.theme.border; }, space_1.default(0.5), space_1.default(1.5), function (p) { return (p.centered ? 'text-align: center;' : ''); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
exports.ListGroupItem = ListGroupItem;
var ListGroup = styled_1.default('ul')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);\n  background: ", ";\n  padding: 0;\n  margin: 0;\n\n  ", "\n"], ["\n  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);\n  background: ", ";\n  padding: 0;\n  margin: 0;\n\n  ", "\n"])), function (p) { return p.theme.background; }, function (p) {
    return p.striped
        ? "\n    & > li:nth-child(odd) {\n      background: " + p.theme.backgroundSecondary + ";\n    }\n  "
        : '';
});
exports.ListGroup = ListGroup;
var templateObject_1, templateObject_2;
//# sourceMappingURL=listGroup.jsx.map