Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var uniqWith_1 = tslib_1.__importDefault(require("lodash/uniqWith"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var errorItem_1 = tslib_1.__importDefault(require("app/components/events/errorItem"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var eventErrors_1 = require("app/constants/eventErrors");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var styles_1 = require("./styles");
var MAX_ERRORS = 100;
var Errors = /** @class */ (function (_super) {
    tslib_1.__extends(Errors, _super);
    function Errors() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.toggle = function () {
            _this.setState(function (state) { return ({ isOpen: !state.isOpen }); });
        };
        return _this;
    }
    Errors.prototype.componentDidMount = function () {
        this.checkSourceCodeErrors();
    };
    Errors.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (this.state.isOpen !== nextState.isOpen) {
            return true;
        }
        return this.props.event.id !== nextProps.event.id;
    };
    Errors.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.event.id !== prevProps.event.id) {
            this.checkSourceCodeErrors();
        }
    };
    Errors.prototype.fetchReleaseArtifacts = function (query) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, orgSlug, event, projectSlug, release, releaseVersion, releaseArtifacts, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgSlug = _a.orgSlug, event = _a.event, projectSlug = _a.projectSlug;
                        release = event.release;
                        releaseVersion = release === null || release === void 0 ? void 0 : release.version;
                        if (!releaseVersion || !query) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/files/?query=" + query, {
                                method: 'GET',
                            })];
                    case 2:
                        releaseArtifacts = _b.sent();
                        this.setState({ releaseArtifacts: releaseArtifacts });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Errors.prototype.checkSourceCodeErrors = function () {
        var e_1, _a;
        var event = this.props.event;
        var errors = event.errors;
        var sourceCodeErrors = (errors !== null && errors !== void 0 ? errors : []).filter(function (error) { return error.type === 'js_no_source' && error.data.url; });
        if (!sourceCodeErrors.length) {
            return;
        }
        var pathNames = [];
        try {
            for (var sourceCodeErrors_1 = tslib_1.__values(sourceCodeErrors), sourceCodeErrors_1_1 = sourceCodeErrors_1.next(); !sourceCodeErrors_1_1.done; sourceCodeErrors_1_1 = sourceCodeErrors_1.next()) {
                var sourceCodeError = sourceCodeErrors_1_1.value;
                var url = sourceCodeError.data.url;
                if (url) {
                    var pathName = this.getURLPathname(url);
                    if (pathName) {
                        pathNames.push(encodeURIComponent(pathName));
                    }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (sourceCodeErrors_1_1 && !sourceCodeErrors_1_1.done && (_a = sourceCodeErrors_1.return)) _a.call(sourceCodeErrors_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.fetchReleaseArtifacts(pathNames.join('&query='));
    };
    Errors.prototype.getURLPathname = function (url) {
        try {
            return new URL(url).pathname;
        }
        catch (_a) {
            return undefined;
        }
    };
    Errors.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, proGuardErrors = _a.proGuardErrors;
        var _b = this.state, isOpen = _b.isOpen, releaseArtifacts = _b.releaseArtifacts;
        var eventDistribution = event.dist, _c = event.errors, eventErrors = _c === void 0 ? [] : _c;
        // XXX: uniqWith returns unique errors and is not performant with large datasets
        var otherErrors = eventErrors.length > MAX_ERRORS ? eventErrors : uniqWith_1.default(eventErrors, isEqual_1.default);
        var errors = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(otherErrors)), tslib_1.__read(proGuardErrors));
        return (<StyledBanner priority="danger">
        <styles_1.BannerSummary>
          <StyledIconWarning />
          <span data-test-id="errors-banner-summary-info">
            {locale_1.tn('There was %s problem processing this event', 'There were %s problems processing this event', errors.length)}
          </span>
          <StyledButton data-test-id="event-error-toggle" priority="link" onClick={this.toggle}>
            {isOpen ? locale_1.t('Hide') : locale_1.t('Show')}
          </StyledButton>
        </styles_1.BannerSummary>
        {isOpen && (<react_1.Fragment>
            <Divider />
            <ErrorList data-test-id="event-error-details" symbol="bullet">
              {errors.map(function (error, errorIdx) {
                    var _a, _b;
                    var data = (_a = error.data) !== null && _a !== void 0 ? _a : {};
                    if (error.type === eventErrors_1.JavascriptProcessingErrors.JS_MISSING_SOURCE &&
                        data.url &&
                        !!(releaseArtifacts === null || releaseArtifacts === void 0 ? void 0 : releaseArtifacts.length)) {
                        var releaseArtifact = releaseArtifacts.find(function (releaseArt) {
                            var pathname = data.url ? _this.getURLPathname(data.url) : undefined;
                            if (pathname) {
                                return releaseArt.name.includes(pathname);
                            }
                            return false;
                        });
                        var releaseArtifactDistribution = (_b = releaseArtifact === null || releaseArtifact === void 0 ? void 0 : releaseArtifact.dist) !== null && _b !== void 0 ? _b : null;
                        // Neither event nor file have dist -> matching
                        // Event has dist, file doesn’t -> not matching
                        // File has dist, event doesn’t -> not matching
                        // Both have dist, same value -> matching
                        // Both have dist, different values -> not matching
                        if (releaseArtifactDistribution !== eventDistribution) {
                            error.message = locale_1.t('Source code was not found because the distribution did not match');
                            data['expected-distribution'] = eventDistribution;
                            data['current-distribution'] = releaseArtifactDistribution;
                        }
                    }
                    return <errorItem_1.default key={errorIdx} error={tslib_1.__assign(tslib_1.__assign({}, error), { data: data })}/>;
                })}
            </ErrorList>
          </react_1.Fragment>)}
      </StyledBanner>);
    };
    return Errors;
}(react_1.Component));
var linkStyle = function (_a) {
    var theme = _a.theme;
    return react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), theme.subText, theme.textColor);
};
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), linkStyle);
var StyledBanner = styled_1.default(styles_1.BannerContainer)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"], ["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"])), linkStyle);
var StyledIconWarning = styled_1.default(icons_1.IconWarning)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
// TODO(theme) don't use a custom pink
var customPink = '#e7c0bc';
var Divider = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: 1px;\n  background-color: ", ";\n"], ["\n  height: 1px;\n  background-color: ", ";\n"])), customPink);
var ErrorList = styled_1.default(list_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", " 0 40px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"], ["\n  margin: 0 ", " 0 40px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"])), space_1.default(4), space_1.default(1), space_1.default(0.5), space_1.default(0.5));
exports.default = withApi_1.default(Errors);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=errors.jsx.map