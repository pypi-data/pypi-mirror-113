Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var framer_motion_1 = require("framer-motion");
var indicator_1 = require("app/actionCreators/indicator");
var projects_1 = require("app/actionCreators/projects");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var platformPicker_1 = tslib_1.__importDefault(require("app/components/platformPicker"));
var locale_1 = require("app/locale");
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var stepHeading_1 = tslib_1.__importDefault(require("./components/stepHeading"));
var OnboardingPlatform = /** @class */ (function (_super) {
    tslib_1.__extends(OnboardingPlatform, _super);
    function OnboardingPlatform() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            firstProjectCreated: false,
            progressing: false,
        };
        _this.handleSetPlatform = function (platform) { return _this.props.onUpdate({ platform: platform }); };
        _this.handleContinue = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var platform;
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ progressing: true });
                        platform = this.props.platform;
                        if (platform === null) {
                            return [2 /*return*/];
                        }
                        advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_set_up_your_project', { platform: platform }, (_a = this.props.organization) !== null && _a !== void 0 ? _a : null);
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        return [4 /*yield*/, this.createFirstProject(platform)];
                    case 1:
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        _b.sent();
                        this.props.onComplete({});
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    OnboardingPlatform.prototype.componentDidMount = function () {
        var _a;
        advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_load_choose_platform', {}, (_a = this.props.organization) !== null && _a !== void 0 ? _a : null);
    };
    OnboardingPlatform.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.active && !this.props.active) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({ progressing: false });
        }
    };
    Object.defineProperty(OnboardingPlatform.prototype, "hasFirstProject", {
        get: function () {
            return this.props.project || this.state.firstProjectCreated;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OnboardingPlatform.prototype, "continueButtonLabel", {
        get: function () {
            if (this.state.progressing) {
                return locale_1.t('Creating Project...');
            }
            if (!this.hasFirstProject) {
                return locale_1.t('Create Project');
            }
            if (!this.props.active) {
                return locale_1.t('Project Created');
            }
            return locale_1.t('Set Up Your Project');
        },
        enumerable: false,
        configurable: true
    });
    OnboardingPlatform.prototype.createFirstProject = function (platform) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, orgId, teams, data, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, teams = _a.teams;
                        if (this.hasFirstProject) {
                            return [2 /*return*/];
                        }
                        if (teams.length < 1) {
                            return [2 /*return*/];
                        }
                        this.setState({ firstProjectCreated: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.createProject(api, orgId, teams[0].slug, orgId, platform, {
                                defaultRules: false,
                            })];
                    case 2:
                        data = _b.sent();
                        projectActions_1.default.createSuccess(data);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Failed to create project'));
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    OnboardingPlatform.prototype.render = function () {
        var _this = this;
        var _a = this.props, active = _a.active, project = _a.project, platform = _a.platform;
        var selectedPlatform = platform || (project && project.platform);
        var continueDisabled = this.state.progressing || (this.hasFirstProject && !active);
        return (<div>
        <stepHeading_1.default step={1}>Choose your project’s platform</stepHeading_1.default>
        <framer_motion_1.motion.div variants={{
                initial: { y: 30, opacity: 0 },
                animate: { y: 0, opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <p>
            {locale_1.tct("Variety is the spice of application monitoring. Sentry SDKs integrate\n             with most languages and platforms your developer heart desires.\n             [link:View the full list].", { link: <externalLink_1.default href="https://docs.sentry.io/platforms/"/> })}
          </p>
          <platformPicker_1.default noAutoFilter platform={selectedPlatform} setPlatform={this.handleSetPlatform} source="Onboarding" organization={this.props.organization}/>
          <p>
            {locale_1.tct("Don't see your platform-of-choice? Fear not. Select\n               [otherPlatformLink:other platform] when using a [communityClient:community client].\n               Need help? Learn more in [docs:our docs].", {
                otherPlatformLink: (<button_1.default priority="link" onClick={function () { return _this.handleSetPlatform('other'); }}/>),
                communityClient: (<externalLink_1.default href="https://docs.sentry.io/platforms/#community-supported"/>),
                docs: <externalLink_1.default href="https://docs.sentry.io/platforms/"/>,
            })}
          </p>
          {selectedPlatform && (<button_1.default data-test-id="platform-select-next" priority="primary" disabled={continueDisabled} onClick={this.handleContinue}>
              {this.continueButtonLabel}
            </button_1.default>)}
        </framer_motion_1.motion.div>
      </div>);
    };
    return OnboardingPlatform;
}(react_1.Component));
exports.default = withApi_1.default(withTeams_1.default(OnboardingPlatform));
//# sourceMappingURL=platform.jsx.map