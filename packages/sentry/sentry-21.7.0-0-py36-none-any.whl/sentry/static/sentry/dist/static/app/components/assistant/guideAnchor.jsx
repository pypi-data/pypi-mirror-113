Object.defineProperty(exports, "__esModule", { value: true });
exports.GuideAnchor = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var guides_1 = require("app/actionCreators/guides");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hovercard_1 = tslib_1.__importStar(require("app/components/hovercard"));
var locale_1 = require("app/locale");
var guideStore_1 = tslib_1.__importDefault(require("app/stores/guideStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
/**
 * A GuideAnchor puts an informative hovercard around an element.
 * Guide anchors register with the GuideStore, which uses registrations
 * from one or more anchors on the page to determine which guides can
 * be shown on the page.
 */
var GuideAnchor = /** @class */ (function (_super) {
    tslib_1.__extends(GuideAnchor, _super);
    function GuideAnchor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            active: false,
            step: 0,
            orgId: null,
        };
        _this.unsubscribe = guideStore_1.default.listen(function (data) { return _this.onGuideStateChange(data); }, undefined);
        _this.containerElement = React.createRef();
        /**
         * Terminology:
         *
         *  - A guide can be FINISHED by clicking one of the buttons in the last step
         *  - A guide can be DISMISSED by x-ing out of it at any step except the last (where there is no x)
         *  - In both cases we consider it CLOSED
         */
        _this.handleFinish = function (e) {
            e.stopPropagation();
            var onFinish = _this.props.onFinish;
            if (onFinish) {
                onFinish();
            }
            var _a = _this.state, currentGuide = _a.currentGuide, orgId = _a.orgId;
            if (currentGuide) {
                guides_1.recordFinish(currentGuide.guide, orgId);
            }
            guides_1.closeGuide();
        };
        _this.handleNextStep = function (e) {
            e.stopPropagation();
            guides_1.nextStep();
        };
        _this.handleDismiss = function (e) {
            e.stopPropagation();
            var _a = _this.state, currentGuide = _a.currentGuide, step = _a.step, orgId = _a.orgId;
            if (currentGuide) {
                guides_1.dismissGuide(currentGuide.guide, step, orgId);
            }
        };
        return _this;
    }
    GuideAnchor.prototype.componentDidMount = function () {
        var target = this.props.target;
        target && guides_1.registerAnchor(target);
    };
    GuideAnchor.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (this.containerElement.current && !prevState.active && this.state.active) {
            try {
                var top_1 = this.containerElement.current.getBoundingClientRect().top;
                var scrollTop = window.pageYOffset;
                var centerElement = top_1 + scrollTop - window.innerHeight / 2;
                window.scrollTo({ top: centerElement });
            }
            catch (err) {
                Sentry.captureException(err);
            }
        }
    };
    GuideAnchor.prototype.componentWillUnmount = function () {
        var target = this.props.target;
        target && guides_1.unregisterAnchor(target);
        this.unsubscribe();
    };
    GuideAnchor.prototype.onGuideStateChange = function (data) {
        var _a, _b, _c, _d;
        var active = (_c = ((_b = (_a = data.currentGuide) === null || _a === void 0 ? void 0 : _a.steps[data.currentStep]) === null || _b === void 0 ? void 0 : _b.target) === this.props.target) !== null && _c !== void 0 ? _c : false;
        this.setState({
            active: active,
            currentGuide: (_d = data.currentGuide) !== null && _d !== void 0 ? _d : undefined,
            step: data.currentStep,
            orgId: data.orgId,
        });
    };
    GuideAnchor.prototype.getHovercardBody = function () {
        var to = this.props.to;
        var _a = this.state, currentGuide = _a.currentGuide, step = _a.step;
        if (!currentGuide) {
            return null;
        }
        var totalStepCount = currentGuide.steps.length;
        var currentStepCount = step + 1;
        var currentStep = currentGuide.steps[step];
        var lastStep = currentStepCount === totalStepCount;
        var hasManySteps = totalStepCount > 1;
        // to clear `#assistant` from the url
        var href = window.location.hash === '#assistant' ? '#' : '';
        var dismissButton = (<DismissButton size="small" href={href} onClick={this.handleDismiss} priority="link">
        {currentStep.dismissText || locale_1.t('Dismiss')}
      </DismissButton>);
        return (<GuideContainer>
        <GuideContent>
          {currentStep.title && <GuideTitle>{currentStep.title}</GuideTitle>}
          <GuideDescription>{currentStep.description}</GuideDescription>
        </GuideContent>
        <GuideAction>
          <div>
            {lastStep ? (<React.Fragment>
                <StyledButton size="small" to={to} onClick={this.handleFinish}>
                  {currentStep.nextText ||
                    (hasManySteps ? locale_1.t('Enough Already') : locale_1.t('Got It'))}
                </StyledButton>
                {currentStep.hasNextGuide && dismissButton}
              </React.Fragment>) : (<React.Fragment>
                <StyledButton size="small" onClick={this.handleNextStep} to={to}>
                  {currentStep.nextText || locale_1.t('Next')}
                </StyledButton>
                {!currentStep.cantDismiss && dismissButton}
              </React.Fragment>)}
          </div>

          {hasManySteps && (<StepCount>
              {locale_1.tct('[currentStepCount] of [totalStepCount]', {
                    currentStepCount: currentStepCount,
                    totalStepCount: totalStepCount,
                })}
            </StepCount>)}
        </GuideAction>
      </GuideContainer>);
    };
    GuideAnchor.prototype.render = function () {
        var _a = this.props, children = _a.children, position = _a.position, offset = _a.offset, containerClassName = _a.containerClassName;
        var active = this.state.active;
        if (!active) {
            return children ? children : null;
        }
        return (<StyledHovercard show body={this.getHovercardBody()} tipColor={theme_1.default.purple300} position={position} offset={offset} containerClassName={containerClassName}>
        <span ref={this.containerElement}>{children}</span>
      </StyledHovercard>);
    };
    return GuideAnchor;
}(React.Component));
exports.GuideAnchor = GuideAnchor;
var GuideAnchorWrapper = /** @class */ (function (_super) {
    tslib_1.__extends(GuideAnchorWrapper, _super);
    function GuideAnchorWrapper() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GuideAnchorWrapper.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, children = _a.children, rest = tslib_1.__rest(_a, ["disabled", "children"]);
        if (disabled || window.localStorage.getItem('hide_anchors') === '1') {
            return children || null;
        }
        return <GuideAnchor {...rest}>{children}</GuideAnchor>;
    };
    return GuideAnchorWrapper;
}(React.Component));
exports.default = GuideAnchorWrapper;
var GuideContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"])), space_1.default(2), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.white; });
var GuideContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space_1.default(1), function (p) { return p.theme.white; });
var GuideTitle = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  font-size: ", ";\n"], ["\n  font-weight: bold;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var GuideDescription = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var GuideAction = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"])), space_1.default(1));
var StyledButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  min-width: 40%;\n"], ["\n  font-size: ", ";\n  min-width: 40%;\n"])), function (p) { return p.theme.fontSizeMedium; });
var DismissButton = styled_1.default(StyledButton)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  color: ", ";\n"], ["\n  margin-left: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.white; }, function (p) { return p.theme.white; });
var StepCount = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledHovercard = styled_1.default(hovercard_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n    width: 300px;\n  }\n"], ["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n    width: 300px;\n  }\n"])), hovercard_1.Body, theme_1.default.purple300, theme_1.default.borderRadius);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=guideAnchor.jsx.map