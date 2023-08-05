Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var congrats_robots_mp4_1 = tslib_1.__importDefault(require("sentry-images/spot/congrats-robots.mp4"));
var autoplayVideo_1 = tslib_1.__importDefault(require("app/components/autoplayVideo"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
/**
 * Note, video needs `muted` for `autoplay` to work on Chrome
 * See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
 */
function CongratsRobots() {
    return (<AnimatedScene>
      <StyledAutoplayVideo src={congrats_robots_mp4_1.default}/>
    </AnimatedScene>);
}
exports.default = CongratsRobots;
var AnimatedScene = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  max-width: 800px;\n"], ["\n  max-width: 800px;\n"])));
var StyledAutoplayVideo = styled_1.default(autoplayVideo_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  max-height: 320px;\n  max-width: 100%;\n  margin-bottom: ", ";\n"], ["\n  max-height: 320px;\n  max-width: 100%;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=congratsRobots.jsx.map