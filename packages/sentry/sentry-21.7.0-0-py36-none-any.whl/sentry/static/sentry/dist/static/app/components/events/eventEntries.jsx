Object.defineProperty(exports, "__esModule", { value: true });
exports.BorderlessEventEntries = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var contexts_1 = tslib_1.__importDefault(require("app/components/events/contexts"));
var contextSummary_1 = tslib_1.__importDefault(require("app/components/events/contextSummary/contextSummary"));
var device_1 = tslib_1.__importDefault(require("app/components/events/device"));
var errors_1 = tslib_1.__importDefault(require("app/components/events/errors"));
var eventAttachments_1 = tslib_1.__importDefault(require("app/components/events/eventAttachments"));
var eventCause_1 = tslib_1.__importDefault(require("app/components/events/eventCause"));
var eventCauseEmpty_1 = tslib_1.__importDefault(require("app/components/events/eventCauseEmpty"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var eventExtraData_1 = tslib_1.__importDefault(require("app/components/events/eventExtraData/eventExtraData"));
var eventSdk_1 = tslib_1.__importDefault(require("app/components/events/eventSdk"));
var eventTags_1 = tslib_1.__importDefault(require("app/components/events/eventTags/eventTags"));
var groupingInfo_1 = tslib_1.__importDefault(require("app/components/events/groupingInfo"));
var packageData_1 = tslib_1.__importDefault(require("app/components/events/packageData"));
var rrwebIntegration_1 = tslib_1.__importDefault(require("app/components/events/rrwebIntegration"));
var sdkUpdates_1 = tslib_1.__importDefault(require("app/components/events/sdkUpdates"));
var styles_1 = require("app/components/events/styles");
var userFeedback_1 = tslib_1.__importDefault(require("app/components/events/userFeedback"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var event_1 = require("app/types/event");
var utils_1 = require("app/types/utils");
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectProcessingIssues_1 = require("app/views/settings/project/projectProcessingIssues");
var findBestThread_1 = tslib_1.__importDefault(require("./interfaces/threads/threadSelector/findBestThread"));
var getThreadException_1 = tslib_1.__importDefault(require("./interfaces/threads/threadSelector/getThreadException"));
var eventEntry_1 = tslib_1.__importDefault(require("./eventEntry"));
var eventTagsAndScreenshot_1 = tslib_1.__importDefault(require("./eventTagsAndScreenshot"));
var MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH = /^(([\w\$]\.[\w\$]{1,2})|([\w\$]{2}\.[\w\$]\.[\w\$]))(\.|$)/g;
var defaultProps = {
    isShare: false,
    showExampleCommit: false,
    showTagSummary: true,
    isBorderless: false,
};
var EventEntries = /** @class */ (function (_super) {
    tslib_1.__extends(EventEntries, _super);
    function EventEntries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            proGuardErrors: [],
        };
        return _this;
    }
    EventEntries.prototype.componentDidMount = function () {
        this.checkProGuardError();
        this.recordIssueError();
    };
    EventEntries.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        var _a = this.props, event = _a.event, showExampleCommit = _a.showExampleCommit;
        return ((event && nextProps.event && event.id !== nextProps.event.id) ||
            showExampleCommit !== nextProps.showExampleCommit ||
            nextState.isLoading !== this.state.isLoading);
    };
    EventEntries.prototype.fetchProguardMappingFiles = function (query) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, project, proguardMappingFiles, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/files/dsyms/", {
                                method: 'GET',
                                query: {
                                    query: query,
                                    file_formats: 'proguard',
                                },
                            })];
                    case 2:
                        proguardMappingFiles = _b.sent();
                        return [2 /*return*/, proguardMappingFiles];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        // do nothing, the UI will not display extra error details
                        return [2 /*return*/, []];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    EventEntries.prototype.isDataMinified = function (str) {
        if (!str) {
            return false;
        }
        return !!tslib_1.__spreadArray([], tslib_1.__read(str.matchAll(MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH))).length;
    };
    EventEntries.prototype.hasThreadOrExceptionMinifiedFrameData = function (event, bestThread) {
        var _this = this;
        var _a, _b, _c, _d, _e, _f, _g;
        if (!bestThread) {
            var exceptionValues = (_d = (_c = (_b = (_a = event.entries) === null || _a === void 0 ? void 0 : _a.find(function (e) { return e.type === event_1.EntryType.EXCEPTION; })) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values) !== null && _d !== void 0 ? _d : [];
            return !!exceptionValues.find(function (exceptionValue) {
                var _a, _b;
                return (_b = (_a = exceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) {
                    return _this.isDataMinified(frame.module);
                });
            });
        }
        var threadExceptionValues = (_e = getThreadException_1.default(event, bestThread)) === null || _e === void 0 ? void 0 : _e.values;
        return !!(threadExceptionValues
            ? threadExceptionValues.find(function (threadExceptionValue) {
                var _a, _b;
                return (_b = (_a = threadExceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) {
                    return _this.isDataMinified(frame.module);
                });
            })
            : (_g = (_f = bestThread === null || bestThread === void 0 ? void 0 : bestThread.stacktrace) === null || _f === void 0 ? void 0 : _f.frames) === null || _g === void 0 ? void 0 : _g.find(function (frame) { return _this.isDataMinified(frame.module); }));
    };
    EventEntries.prototype.checkProGuardError = function () {
        var _a, _b, _c, _d, _e, _f, _g;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _h, event, isShare, hasEventErrorsProGuardMissingMapping, proGuardErrors, debugImages, proGuardImage, proGuardImageUuid, proguardMappingFiles, threads, bestThread, hasThreadOrExceptionMinifiedData;
            return tslib_1.__generator(this, function (_j) {
                switch (_j.label) {
                    case 0:
                        _h = this.props, event = _h.event, isShare = _h.isShare;
                        if (!event || event.platform !== 'java') {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        hasEventErrorsProGuardMissingMapping = (_a = event.errors) === null || _a === void 0 ? void 0 : _a.find(function (error) { return error.type === 'proguard_missing_mapping'; });
                        if (hasEventErrorsProGuardMissingMapping) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        proGuardErrors = [];
                        debugImages = (_c = (_b = event.entries) === null || _b === void 0 ? void 0 : _b.find(function (e) { return e.type === event_1.EntryType.DEBUGMETA; })) === null || _c === void 0 ? void 0 : _c.data.images;
                        proGuardImage = debugImages === null || debugImages === void 0 ? void 0 : debugImages.find(function (debugImage) { return (debugImage === null || debugImage === void 0 ? void 0 : debugImage.type) === 'proguard'; });
                        proGuardImageUuid = proGuardImage === null || proGuardImage === void 0 ? void 0 : proGuardImage.uuid;
                        if (!utils_2.defined(proGuardImageUuid)) return [3 /*break*/, 2];
                        if (isShare) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.fetchProguardMappingFiles(proGuardImageUuid)];
                    case 1:
                        proguardMappingFiles = _j.sent();
                        if (!proguardMappingFiles.length) {
                            proGuardErrors.push({
                                type: 'proguard_missing_mapping',
                                message: projectProcessingIssues_1.projectProcessingIssuesMessages.proguard_missing_mapping,
                                data: { mapping_uuid: proGuardImageUuid },
                            });
                        }
                        this.setState({ proGuardErrors: proGuardErrors, isLoading: false });
                        return [2 /*return*/];
                    case 2:
                        if (proGuardImage) {
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage('Event contains proguard image but not uuid');
                            });
                        }
                        _j.label = 3;
                    case 3:
                        threads = (_g = (_f = (_e = (_d = event.entries) === null || _d === void 0 ? void 0 : _d.find(function (e) { return e.type === event_1.EntryType.THREADS; })) === null || _e === void 0 ? void 0 : _e.data) === null || _f === void 0 ? void 0 : _f.values) !== null && _g !== void 0 ? _g : [];
                        bestThread = findBestThread_1.default(threads);
                        hasThreadOrExceptionMinifiedData = this.hasThreadOrExceptionMinifiedFrameData(event, bestThread);
                        if (hasThreadOrExceptionMinifiedData) {
                            proGuardErrors.push({
                                type: 'proguard_potentially_misconfigured_plugin',
                                message: locale_1.tct('Some frames appear to be minified. Did you configure the [plugin]?', {
                                    plugin: (<externalLink_1.default href="https://docs.sentry.io/platforms/android/proguard/#gradle">
                Sentry Gradle Plugin
              </externalLink_1.default>),
                                }),
                            });
                            // This capture will be removed once we're confident with the level of effectiveness
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage(!proGuardImage
                                    ? 'No Proguard is used at all, but a frame did match the regex'
                                    : "Displaying ProGuard warning 'proguard_potentially_misconfigured_plugin' for suspected event");
                            });
                        }
                        this.setState({ proGuardErrors: proGuardErrors, isLoading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventEntries.prototype.recordIssueError = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        var errors = event.errors;
        var errorTypes = errors.map(function (errorEntries) { return errorEntries.type; });
        var errorMessages = errors.map(function (errorEntries) { return errorEntries.message; });
        var orgId = organization.id;
        var platform = project.platform;
        analytics_1.analytics('issue_error_banner.viewed', tslib_1.__assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform: platform })));
    };
    EventEntries.prototype.renderEntries = function (event) {
        var _a = this.props, project = _a.project, organization = _a.organization, group = _a.group;
        var entries = event.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map(function (entry, entryIdx) { return (<errorBoundary_1.default key={"entry-" + entryIdx} customComponent={<eventDataSection_1.default type={entry.type} title={entry.type}>
            <p>{locale_1.t('There was an error rendering this data.')}</p>
          </eventDataSection_1.default>}>
        <eventEntry_1.default projectSlug={project.slug} groupId={group === null || group === void 0 ? void 0 : group.id} organization={organization} event={event} entry={entry}/>
      </errorBoundary_1.default>); });
    };
    EventEntries.prototype.render = function () {
        var _a;
        var _b = this.props, className = _b.className, organization = _b.organization, group = _b.group, isShare = _b.isShare, project = _b.project, event = _b.event, showExampleCommit = _b.showExampleCommit, showTagSummary = _b.showTagSummary, location = _b.location, isBorderless = _b.isBorderless;
        var _c = this.state, proGuardErrors = _c.proGuardErrors, isLoading = _c.isLoading;
        var features = new Set(organization === null || organization === void 0 ? void 0 : organization.features);
        var hasQueryFeature = features.has('discover-query');
        var hasMobileScreenshotsFeature = features.has('mobile-screenshots');
        if (!event) {
            return (<div style={{ padding: '15px 30px' }}>
          <h3>{locale_1.t('Latest Event Not Available')}</h3>
        </div>);
        }
        var hasContext = !utils_2.objectIsEmpty(event.user) || !utils_2.objectIsEmpty(event.contexts);
        var hasErrors = !utils_2.objectIsEmpty(event.errors) || !!proGuardErrors.length;
        return (<div className={className} data-test-id={"event-entries-loading-" + isLoading}>
        {hasErrors && !isLoading && (<errors_1.default event={event} orgSlug={organization.slug} projectSlug={project.slug} proGuardErrors={proGuardErrors}/>)}
        {!isShare &&
                utils_1.isNotSharedOrganization(organization) &&
                (showExampleCommit ? (<eventCauseEmpty_1.default event={event} organization={organization} project={project}/>) : (<eventCause_1.default organization={organization} project={project} event={event} group={group}/>))}
        {(event === null || event === void 0 ? void 0 : event.userReport) && group && (<StyledEventUserFeedback report={event.userReport} orgId={organization.slug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {showTagSummary &&
                (hasMobileScreenshotsFeature ? (<eventTagsAndScreenshot_1.default event={event} organization={organization} projectId={project.slug} location={location} hasQueryFeature={hasQueryFeature} isShare={isShare} hasContext={hasContext} isBorderless={isBorderless}/>) : ((!!((_a = event.tags) !== null && _a !== void 0 ? _a : []).length || hasContext) && (<StyledEventDataSection title={locale_1.t('Tags')} type="tags">
                {hasContext && <contextSummary_1.default event={event}/>}
                <eventTags_1.default event={event} organization={organization} projectId={project.slug} location={location} hasQueryFeature={hasQueryFeature}/>
              </StyledEventDataSection>)))}
        {this.renderEntries(event)}
        {hasContext && <contexts_1.default group={group} event={event}/>}
        {event && !utils_2.objectIsEmpty(event.context) && <eventExtraData_1.default event={event}/>}
        {event && !utils_2.objectIsEmpty(event.packages) && <packageData_1.default event={event}/>}
        {event && !utils_2.objectIsEmpty(event.device) && <device_1.default event={event}/>}
        {!isShare && features.has('event-attachments') && (<eventAttachments_1.default event={event} orgId={organization.slug} projectId={project.slug} location={location}/>)}
        {(event === null || event === void 0 ? void 0 : event.sdk) && !utils_2.objectIsEmpty(event.sdk) && <eventSdk_1.default sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<sdkUpdates_1.default event={tslib_1.__assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && (event === null || event === void 0 ? void 0 : event.groupID) && (<groupingInfo_1.default projectId={project.slug} event={event} showGroupingConfig={features.has('set-grouping-config')}/>)}
        {!isShare && features.has('event-attachments') && (<rrwebIntegration_1.default event={event} orgId={organization.slug} projectId={project.slug}/>)}
      </div>);
    };
    EventEntries.defaultProps = defaultProps;
    return EventEntries;
}(react_1.Component));
var ErrorContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"], ["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"])));
var BorderlessEventEntries = styled_1.default(EventEntries)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  & ", " {\n    padding: ", " 0 0 0;\n  }\n  & ", ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & ", " {\n    margin-bottom: ", ";\n  }\n"], ["\n  & " /* sc-selector */, " {\n    padding: ", " 0 0 0;\n  }\n  & " /* sc-selector */, ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & " /* sc-selector */, " {\n    margin-bottom: ", ";\n  }\n"])), /* sc-selector */ styles_1.DataSection, space_1.default(3), /* sc-selector */ styles_1.DataSection, /* sc-selector */ ErrorContainer, space_1.default(2));
exports.BorderlessEventEntries = BorderlessEventEntries;
var StyledEventUserFeedback = styled_1.default(userFeedback_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"], ["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"])), function (p) { return (p.includeBorder ? "border-top: 1px solid " + p.theme.innerBorder + ";" : ''); });
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
// TODO(ts): any required due to our use of SharedViewOrganization
exports.default = withOrganization_1.default(withApi_1.default(EventEntries));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventEntries.jsx.map