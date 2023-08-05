Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hook_1 = tslib_1.__importDefault(require("app/components/hook"));
var logoSentry_1 = tslib_1.__importDefault(require("app/components/logoSentry"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var pageCorners_1 = tslib_1.__importDefault(require("./components/pageCorners"));
var platform_1 = tslib_1.__importDefault(require("./platform"));
var sdkConfiguration_1 = tslib_1.__importDefault(require("./sdkConfiguration"));
var welcome_1 = tslib_1.__importDefault(require("./welcome"));
var ONBOARDING_STEPS = [
    {
        id: 'welcome',
        title: locale_1.t('Welcome to Sentry'),
        Component: welcome_1.default,
        centered: true,
    },
    {
        id: 'select-platform',
        title: locale_1.t('Select a platform'),
        Component: platform_1.default,
    },
    {
        id: 'get-started',
        title: locale_1.t('Install the Sentry SDK'),
        Component: sdkConfiguration_1.default,
    },
];
var Onboarding = /** @class */ (function (_super) {
    tslib_1.__extends(Onboarding, _super);
    function Onboarding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleUpdate = function (data) {
            _this.setState(data);
        };
        _this.handleGoBack = function () {
            var previousStep = _this.props.steps[_this.activeStepIndex - 1];
            react_router_1.browserHistory.replace("/onboarding/" + _this.props.params.orgId + "/" + previousStep.id + "/");
        };
        _this.Contents = function () {
            var cornerVariantControl = framer_motion_1.useAnimation();
            var updateCornerVariant = function () {
                cornerVariantControl.start(_this.activeStepIndex === 0 ? 'top-right' : 'top-left');
            };
            // XXX(epurkhiser): We're using a react hook here becuase there's no other
            // way to create framer-motion controls than by using the `useAnimation`
            // hook.
            React.useEffect(updateCornerVariant, []);
            return (<Container>
        <Back animate={_this.activeStepIndex > 0 ? 'visible' : 'hidden'} onClick={_this.handleGoBack}/>
        <framer_motion_1.AnimatePresence exitBeforeEnter onExitComplete={updateCornerVariant}>
          {_this.renderOnboardingStep()}
        </framer_motion_1.AnimatePresence>
        <pageCorners_1.default animateVariant={cornerVariantControl}/>
      </Container>);
        };
        return _this;
    }
    Onboarding.prototype.componentDidMount = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.componentDidUpdate = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.validateActiveStep = function () {
        if (this.activeStepIndex === -1) {
            var firstStep = this.props.steps[0].id;
            react_router_1.browserHistory.replace("/onboarding/" + this.props.params.orgId + "/" + firstStep + "/");
        }
    };
    Object.defineProperty(Onboarding.prototype, "activeStepIndex", {
        get: function () {
            var _this = this;
            return this.props.steps.findIndex(function (_a) {
                var id = _a.id;
                return _this.props.params.step === id;
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "activeStep", {
        get: function () {
            return this.props.steps[this.activeStepIndex];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "firstProject", {
        get: function () {
            var sortedProjects = this.props.projects.sort(function (a, b) { return new Date(a.dateCreated).getTime() - new Date(b.dateCreated).getTime(); });
            return sortedProjects.length > 0 ? sortedProjects[0] : null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "projectPlatform", {
        get: function () {
            var _a, _b, _c;
            return (_c = (_a = this.state.platform) !== null && _a !== void 0 ? _a : (_b = this.firstProject) === null || _b === void 0 ? void 0 : _b.platform) !== null && _c !== void 0 ? _c : null;
        },
        enumerable: false,
        configurable: true
    });
    Onboarding.prototype.handleNextStep = function (step, data) {
        this.handleUpdate(data);
        if (step !== this.activeStep) {
            return;
        }
        var orgId = this.props.params.orgId;
        var nextStep = this.props.steps[this.activeStepIndex + 1];
        react_router_1.browserHistory.push("/onboarding/" + orgId + "/" + nextStep.id + "/");
    };
    Onboarding.prototype.renderProgressBar = function () {
        var activeStepIndex = this.activeStepIndex;
        return (<ProgressBar>
        {this.props.steps.map(function (step, index) { return (<ProgressStep active={activeStepIndex === index} key={step.id}/>); })}
      </ProgressBar>);
    };
    Onboarding.prototype.renderOnboardingStep = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var step = this.activeStep;
        return (<OnboardingStep centered={step.centered} key={step.id} data-test-id={"onboarding-step-" + step.id}>
        <step.Component active orgId={orgId} project={this.firstProject} platform={this.projectPlatform} onComplete={function (data) { return _this.handleNextStep(step, data); }} onUpdate={this.handleUpdate} organization={this.props.organization}/>
      </OnboardingStep>);
    };
    Onboarding.prototype.render = function () {
        if (this.activeStepIndex === -1) {
            return null;
        }
        return (<OnboardingWrapper>
        <react_document_title_1.default title={this.activeStep.title}/>
        <Header>
          <LogoSvg />
          <HeaderRight>
            {this.renderProgressBar()}
            <hook_1.default name="onboarding:extra-chrome"/>
          </HeaderRight>
        </Header>
        <this.Contents />
      </OnboardingWrapper>);
    };
    Onboarding.defaultProps = {
        steps: ONBOARDING_STEPS,
    };
    return Onboarding;
}(React.Component));
var OnboardingWrapper = styled_1.default('main')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n"], ["\n  overflow: hidden;\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n"])));
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  position: relative;\n  background: ", ";\n  padding: 120px ", ";\n  padding-top: 12vh;\n  width: 100%;\n  margin: 0 auto;\n  flex-grow: 1;\n"], ["\n  display: flex;\n  justify-content: center;\n  position: relative;\n  background: ", ";\n  padding: 120px ", ";\n  padding-top: 12vh;\n  width: 100%;\n  margin: 0 auto;\n  flex-grow: 1;\n"])), function (p) { return p.theme.background; }, space_1.default(3));
var Header = styled_1.default('header')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  padding: ", ";\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);\n  display: flex;\n  justify-content: space-between;\n"], ["\n  background: ", ";\n  padding: ", ";\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);\n  display: flex;\n  justify-content: space-between;\n"])), function (p) { return p.theme.background; }, space_1.default(4));
var LogoSvg = styled_1.default(logoSentry_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var ProgressBar = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  min-width: 120px;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"], ["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  min-width: 120px;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"])), space_1.default(4), function (p) { return p.theme.inactive; });
var ProgressStep = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"], ["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"])), function (p) { return (p.active ? p.theme.active : p.theme.inactive); }, function (p) { return p.theme.background; });
var ProgressStatus = styled_1.default(framer_motion_1.motion.div)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var HeaderRight = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"])), space_1.default(1));
ProgressStatus.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: testableTransition_1.default(),
};
var Back = styled_1.default(function (_a) {
    var className = _a.className, animate = _a.animate, props = tslib_1.__rest(_a, ["className", "animate"]);
    return (<framer_motion_1.motion.div className={className} animate={animate} transition={testableTransition_1.default()} variants={{
            initial: { opacity: 0 },
            visible: { opacity: 1, transition: testableTransition_1.default({ delay: 1 }) },
            hidden: { opacity: 0 },
        }}>
    <button_1.default {...props} icon={<icons_1.IconChevron direction="left" size="sm"/>} priority="link">
      {locale_1.t('Go back')}
    </button_1.default>
  </framer_motion_1.motion.div>);
})(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 40px;\n  left: 20px;\n\n  button {\n    font-size: ", ";\n    color: ", ";\n  }\n"], ["\n  position: absolute;\n  top: 40px;\n  left: 20px;\n\n  button {\n    font-size: ", ";\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; });
var OnboardingStep = styled_1.default(framer_motion_1.motion.div)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  width: 850px;\n  display: flex;\n  flex-direction: column;\n  ", ";\n"], ["\n  width: 850px;\n  display: flex;\n  flex-direction: column;\n  ", ";\n"])), function (p) {
    return p.centered &&
        "justify-content: center;\n     align-items: center;";
});
OnboardingStep.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: { animate: {} },
    transition: testableTransition_1.default({
        staggerChildren: 0.2,
    }),
};
exports.default = withOrganization_1.default(withProjects_1.default(Onboarding));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=onboarding.jsx.map