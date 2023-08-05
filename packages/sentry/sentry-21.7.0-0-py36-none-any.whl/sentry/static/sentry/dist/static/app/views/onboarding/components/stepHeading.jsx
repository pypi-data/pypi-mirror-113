Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var StepHeading = styled_1.default(framer_motion_1.motion.h2)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: calc(-", " - 30px);\n  position: relative;\n  display: inline-grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n\n  &:before {\n    content: '", "';\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: ", ";\n    font-size: 1.5rem;\n  }\n"], ["\n  margin-left: calc(-", " - 30px);\n  position: relative;\n  display: inline-grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n\n  &:before {\n    content: '", "';\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: ", ";\n    font-size: 1.5rem;\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.step; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.textColor; });
StepHeading.defaultProps = {
    variants: {
        initial: { clipPath: 'inset(0% 100% 0% 0%)', opacity: 1 },
        animate: { clipPath: 'inset(0% 0% 0% 0%)', opacity: 1 },
        exit: { opacity: 0 },
    },
    transition: testableTransition_1.default({
        duration: 0.3,
    }),
};
exports.default = StepHeading;
var templateObject_1;
//# sourceMappingURL=stepHeading.jsx.map