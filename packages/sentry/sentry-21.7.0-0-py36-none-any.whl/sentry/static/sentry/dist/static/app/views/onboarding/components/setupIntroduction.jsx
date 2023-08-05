Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var platformicons_1 = require("platformicons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var stepHeading_1 = tslib_1.__importDefault(require("./stepHeading"));
function SetupIntroduction(_a) {
    var stepHeaderText = _a.stepHeaderText, platform = _a.platform;
    return (<TitleContainer>
      <stepHeading_1.default step={2}>{stepHeaderText}</stepHeading_1.default>
      <framer_motion_1.motion.div variants={{
            initial: { opacity: 0, x: 20 },
            animate: { opacity: 1, x: 0 },
            exit: { opacity: 0 },
        }}>
        <platformicons_1.PlatformIcon size={48} format="lg" platform={platform}/>
      </framer_motion_1.motion.div>
    </TitleContainer>);
}
exports.default = SetupIntroduction;
var TitleContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  justify-items: end;\n\n  ", " {\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  justify-items: end;\n\n  ", " {\n    margin-bottom: 0;\n  }\n"])), space_1.default(2), stepHeading_1.default);
var templateObject_1;
//# sourceMappingURL=setupIntroduction.jsx.map