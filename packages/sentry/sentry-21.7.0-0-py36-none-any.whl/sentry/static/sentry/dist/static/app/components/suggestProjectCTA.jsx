Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var prompts_1 = require("app/actionCreators/prompts");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var suggestProjectModal_1 = tslib_1.__importDefault(require("app/components/modals/suggestProjectModal"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var MOBILE_PLATFORMS = [
    'react-native',
    'android',
    'cordova',
    'cocoa',
    'cocoa-swift',
    'apple-ios',
    'swift',
    'flutter',
    'xamarin',
    'dotnet-xamarin',
];
var MOBILE_USER_AGENTS = ['okhttp', 'CFNetwork', 'Alamofire', 'Dalvik'];
var SuggestProjectCTA = /** @class */ (function (_super) {
    tslib_1.__extends(SuggestProjectCTA, _super);
    function SuggestProjectCTA() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleCTAClose = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.dismissed_mobile_prompt_banner', {
                matchedUserAgentString: _this.matchedUserAgentString,
            }, _this.props.organization);
            prompts_1.promptsUpdate(api, {
                organizationId: organization.id,
                feature: 'suggest_mobile_project',
                status: 'dismissed',
            });
            _this.setState({ isDismissed: true });
        };
        _this.openModal = function () {
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.opened_mobile_project_suggest_modal', {
                matchedUserAgentString: _this.matchedUserAgentString,
            }, _this.props.organization);
            modal_1.openModal(function (deps) { return (<suggestProjectModal_1.default organization={_this.props.organization} matchedUserAgentString={_this.matchedUserAgentString} {...deps}/>); });
        };
        return _this;
    }
    SuggestProjectCTA.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Object.defineProperty(SuggestProjectCTA.prototype, "matchedUserAgentString", {
        // Returns the matched user agent string
        // otherwise, returns an empty string
        get: function () {
            var _a, _b, _c, _d;
            var entries = this.props.event.entries;
            var requestEntry = entries.find(function (item) { return item.type === 'request'; });
            if (!requestEntry) {
                return '';
            }
            // find the user agent header out of our list of headers
            var userAgent = (_c = (_b = (_a = requestEntry) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.headers) === null || _c === void 0 ? void 0 : _c.find(function (item) { return item[0].toLowerCase() === 'user-agent'; });
            if (!userAgent) {
                return '';
            }
            // check if any of our mobile agent headers matches the event mobile agent
            return ((_d = MOBILE_USER_AGENTS.find(function (mobileAgent) { var _a; return (_a = userAgent[1]) === null || _a === void 0 ? void 0 : _a.toLowerCase().includes(mobileAgent.toLowerCase()); })) !== null && _d !== void 0 ? _d : '');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "hasMobileProject", {
        // check our projects to see if there is a mobile project
        get: function () {
            return this.props.projects.some(function (project) {
                return MOBILE_PLATFORMS.includes(project.platform || '');
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "hasMobileEvent", {
        // returns true if the current event is mobile from the user agent
        // or if we found a mobile event with the API
        get: function () {
            var mobileEventResult = this.state.mobileEventResult;
            return !!this.matchedUserAgentString || !!mobileEventResult;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "showCTA", {
        /**
         * conditions to show prompt:
         * 1. Have a mobile event
         * 2. No mobile project
         * 3. CTA is not dimissed
         * 4. We've loaded the data from the backend for the prompt
         */
        get: function () {
            var _a = this.state, loaded = _a.loaded, isDismissed = _a.isDismissed;
            return !!(this.hasMobileEvent && !this.hasMobileProject && !isDismissed && loaded);
        },
        enumerable: false,
        configurable: true
    });
    SuggestProjectCTA.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, isDismissed, mobileEventResult;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, Promise.all([
                            this.checkMobilePrompt(),
                            this.checkOrgHasMobileEvent(),
                        ])];
                    case 1:
                        _a = tslib_1.__read.apply(void 0, [_b.sent(), 2]), isDismissed = _a[0], mobileEventResult = _a[1];
                        // set the new state
                        this.setState({
                            isDismissed: isDismissed,
                            mobileEventResult: mobileEventResult,
                            loaded: true,
                        }, function () {
                            var matchedUserAgentString = _this.matchedUserAgentString;
                            if (_this.showCTA) {
                                // now record the results
                                advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.show_mobile_prompt_banner', {
                                    matchedUserAgentString: matchedUserAgentString,
                                    mobileEventBrowserName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.browserName) || '',
                                    mobileEventClientOsName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.clientOsName) || '',
                                }, _this.props.organization, { startSession: true });
                            }
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    SuggestProjectCTA.prototype.checkOrgHasMobileEvent = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization;
            return tslib_1.__generator(this, function (_b) {
                _a = this.props, api = _a.api, organization = _a.organization;
                return [2 /*return*/, api.requestPromise("/organizations/" + organization.slug + "/has-mobile-app-events/", {
                        query: {
                            userAgents: MOBILE_USER_AGENTS,
                        },
                    })];
            });
        });
    };
    SuggestProjectCTA.prototype.checkMobilePrompt = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, promptData;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                organizationId: organization.id,
                                feature: 'suggest_mobile_project',
                            })];
                    case 1:
                        promptData = _b.sent();
                        return [2 /*return*/, promptIsDismissed_1.promptIsDismissed(promptData)];
                }
            });
        });
    };
    SuggestProjectCTA.prototype.renderCTA = function () {
        return (<alert_1.default type="info">
        <Content>
          <span>
            {locale_1.tct('We have a sneaking suspicion you have a mobile app that doesn’t use Sentry. [link:Start Monitoring]', { link: <a onClick={this.openModal}/> })}
          </span>
          <StyledIconClose onClick={this.handleCTAClose}/>
        </Content>
      </alert_1.default>);
    };
    SuggestProjectCTA.prototype.render = function () {
        return this.showCTA ? this.renderCTA() : null;
    };
    return SuggestProjectCTA;
}(react_1.Component));
exports.default = withApi_1.default(withProjects_1.default(SuggestProjectCTA));
var Content = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"])), space_1.default(1));
var StyledIconClose = styled_1.default(icons_1.IconClose)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: auto;\n  cursor: pointer;\n"], ["\n  margin: auto;\n  cursor: pointer;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=suggestProjectCTA.jsx.map