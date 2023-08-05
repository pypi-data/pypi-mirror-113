Object.defineProperty(exports, "__esModule", { value: true });
exports.Indicator = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var pulsingIndicator_1 = tslib_1.__importDefault(require("app/styles/pulsingIndicator"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var eventWaiter_1 = tslib_1.__importDefault(require("app/utils/eventWaiter"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var FirstEventIndicator = function (_a) {
    var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
    return (<eventWaiter_1.default {...props}>
    {function (_a) {
            var firstIssue = _a.firstIssue;
            return children({
                indicator: <Indicator firstIssue={firstIssue} {...props}/>,
                firstEventButton: (<button_1.default title={locale_1.t("You'll need to send your first error to continue")} tooltipProps={{ disabled: !!firstIssue }} disabled={!firstIssue} priority="primary" onClick={function () {
                        return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_take_to_error', {}, props.organization);
                    }} to={"/organizations/" + props.organization.slug + "/issues/" + (firstIssue !== true && firstIssue !== null ? firstIssue.id + "/" : '')}>
            {locale_1.t('Take me to my error')}
          </button_1.default>),
            });
        }}
  </eventWaiter_1.default>);
};
var Indicator = function (_a) {
    var firstIssue = _a.firstIssue;
    return (<Container>
    <framer_motion_1.AnimatePresence>
      {!firstIssue ? <Waiting key="waiting"/> : <Success key="received"/>}
    </framer_motion_1.AnimatePresence>
  </Container>);
};
exports.Indicator = Indicator;
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  justify-content: right;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  justify-content: right;\n"])));
var StatusWrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; });
StatusWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: {
        initial: { opacity: 0, y: -10 },
        animate: {
            opacity: 1,
            y: 0,
            transition: testableTransition_1.default({ when: 'beforeChildren', staggerChildren: 0.35 }),
        },
        exit: { opacity: 0, y: 10 },
    },
};
var Waiting = function (props) { return (<StatusWrapper {...props}>
    <AnimatedText>{locale_1.t('Waiting to receive first event to continue')}</AnimatedText>
    <WaitingIndicator />
  </StatusWrapper>); };
var Success = function (props) { return (<StatusWrapper {...props}>
    <AnimatedText>{locale_1.t('Event was received!')}</AnimatedText>
    <ReceivedIndicator />
  </StatusWrapper>); };
var indicatorAnimation = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
};
var AnimatedText = styled_1.default(framer_motion_1.motion.div)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
AnimatedText.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition_1.default(),
};
var WaitingIndicator = styled_1.default(framer_motion_1.motion.div)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0 6px;\n  ", ";\n"], ["\n  margin: 0 6px;\n  ", ";\n"])), pulsingIndicator_1.default);
WaitingIndicator.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition_1.default(),
};
var ReceivedIndicator = styled_1.default(icons_1.IconCheckmark)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 3px;\n  margin: 0 ", ";\n"], ["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 3px;\n  margin: 0 ", ";\n"])), function (p) { return p.theme.green300; }, space_1.default(0.25));
ReceivedIndicator.defaultProps = {
    size: 'sm',
};
exports.default = FirstEventIndicator;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=firstEventIndicator.jsx.map