Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var platformicons_1 = require("platformicons");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var fallingError_1 = tslib_1.__importDefault(require("./components/fallingError"));
var welcomeBackground_1 = tslib_1.__importDefault(require("./components/welcomeBackground"));
var easterEggText = [
    locale_1.t('Be careful. She’s barely hanging on as it is.'),
    locale_1.t("You know this error's not real, right?"),
    locale_1.t("It's that big button, right up there."),
    locale_1.t('You could do this all day. But you really shouldn’t.'),
    locale_1.tct("Ok, really, that's enough. Click [ready:I'm Ready].", { ready: <em /> }),
    locale_1.tct("Next time you do that, [bold:we're starting].", { bold: <strong /> }),
    locale_1.t("We weren't kidding, let's get going."),
];
var fadeAway = {
    variants: {
        initial: { opacity: 0 },
        animate: { opacity: 1, filter: 'blur(0px)' },
        exit: { opacity: 0, filter: 'blur(1px)' },
    },
    transition: testableTransition_1.default({ duration: 0.8 }),
};
var OnboardingWelcome = /** @class */ (function (_super) {
    tslib_1.__extends(OnboardingWelcome, _super);
    function OnboardingWelcome() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OnboardingWelcome.prototype.componentDidMount = function () {
        var _a;
        // Next step will render the platform picker (using both large and small
        // icons). Keep things smooth by prefetching them. Preload a bit late to
        // avoid jank on welcome animations.
        setTimeout(platformicons_1.preloadIcons, 1500);
        advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_start_onboarding', {}, (_a = this.props.organization) !== null && _a !== void 0 ? _a : null);
    };
    OnboardingWelcome.prototype.render = function () {
        var _a = this.props, onComplete = _a.onComplete, active = _a.active;
        return (<fallingError_1.default onFall={function (fallCount) { return fallCount >= easterEggText.length && onComplete({}); }}>
        {function (_a) {
                var fallingError = _a.fallingError, fallCount = _a.fallCount, triggerFall = _a.triggerFall;
                return (<Wrapper>
            <welcomeBackground_1.default />
            <framer_motion_1.motion.h1 {...fadeAway}>{locale_1.t('Welcome to Sentry')}</framer_motion_1.motion.h1>
            <framer_motion_1.motion.p {...fadeAway}>
              {locale_1.t('Find the errors and performance slowdowns that keep you up at night. In two steps.')}
            </framer_motion_1.motion.p>
            <CTAContainer {...fadeAway}>
              <button_1.default data-test-id="welcome-next" disabled={!active} priority="primary" onClick={function () {
                        triggerFall();
                        onComplete({});
                    }}>
                {locale_1.t("I'm Ready")}
              </button_1.default>
              <PositionedFallingError>{fallingError}</PositionedFallingError>
            </CTAContainer>
            <SecondaryAction {...fadeAway}>
              {fallCount > 0 ? easterEggText[fallCount - 1] : <br />}
            </SecondaryAction>
          </Wrapper>);
            }}
      </fallingError_1.default>);
    };
    return OnboardingWelcome;
}(react_1.Component));
var CTAContainer = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  position: relative;\n\n  button {\n    position: relative;\n    z-index: 2;\n  }\n"], ["\n  margin-bottom: ", ";\n  position: relative;\n\n  button {\n    position: relative;\n    z-index: 2;\n  }\n"])), space_1.default(2));
var PositionedFallingError = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  position: absolute;\n  top: 30px;\n  right: -5px;\n  z-index: 0;\n"], ["\n  display: block;\n  position: absolute;\n  top: 30px;\n  right: -5px;\n  z-index: 0;\n"])));
var SecondaryAction = styled_1.default(framer_motion_1.motion.small)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-top: 100px;\n"], ["\n  color: ", ";\n  margin-top: 100px;\n"])), function (p) { return p.theme.subText; });
var Wrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  max-width: 400px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  padding-top: 100px;\n\n  h1 {\n    font-size: 42px;\n  }\n"], ["\n  max-width: 400px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  padding-top: 100px;\n\n  h1 {\n    font-size: 42px;\n  }\n"])));
Wrapper.defaultProps = {
    variants: { exit: { x: 0 } },
    transition: testableTransition_1.default({
        staggerChildren: 0.2,
    }),
};
exports.default = OnboardingWelcome;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=welcome.jsx.map