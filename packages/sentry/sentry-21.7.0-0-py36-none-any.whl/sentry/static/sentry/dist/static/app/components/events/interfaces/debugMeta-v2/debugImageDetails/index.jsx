Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var indicator_1 = require("app/actionCreators/indicator");
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var debugFiles_1 = require("app/types/debugFiles");
var debugImage_1 = require("app/types/debugImage");
var displayReprocessEventAction_1 = require("app/utils/displayReprocessEventAction");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var utils_1 = require("app/views/settings/projectDebugFiles/utils");
var utils_2 = require("../utils");
var candidates_1 = tslib_1.__importDefault(require("./candidates"));
var generalInfo_1 = tslib_1.__importDefault(require("./generalInfo"));
var utils_3 = require("./utils");
var DebugImageDetails = /** @class */ (function (_super) {
    tslib_1.__extends(DebugImageDetails, _super);
    function DebugImageDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (debugId) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, projectId, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, projectId = _a.projectId;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugId, { method: 'DELETE' })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        indicator_1.addErrorMessage(locale_1.t('An error occurred while deleting the debug file.'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    DebugImageDetails.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { debugFiles: [], builtinSymbolSources: [] });
    };
    DebugImageDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!prevProps.image && !!this.props.image) {
            this.remountComponent();
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    DebugImageDetails.prototype.getUplodedDebugFiles = function (candidates) {
        return candidates.find(function (candidate) { return candidate.source === utils_3.INTERNAL_SOURCE; });
    };
    DebugImageDetails.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, image = _a.image;
        if (!image) {
            return [];
        }
        var debug_id = image.debug_id, _b = image.candidates, candidates = _b === void 0 ? [] : _b;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var uploadedDebugFiles = this.getUplodedDebugFiles(candidates);
        var endpoints = [];
        if (uploadedDebugFiles) {
            endpoints.push([
                'debugFiles',
                "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?debug_id=" + debug_id,
                {
                    query: {
                        file_formats: ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle'],
                    },
                },
            ]);
        }
        if (!(builtinSymbolSources === null || builtinSymbolSources === void 0 ? void 0 : builtinSymbolSources.length) &&
            organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    DebugImageDetails.prototype.sortCandidates = function (candidates, unAppliedCandidates) {
        var _a = tslib_1.__read(partition_1.default(candidates, function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.NO_PERMISSION; }), 2), noPermissionCandidates = _a[0], restNoPermissionCandidates = _a[1];
        var _b = tslib_1.__read(partition_1.default(restNoPermissionCandidates, function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.MALFORMED; }), 2), malFormedCandidates = _b[0], restMalFormedCandidates = _b[1];
        var _c = tslib_1.__read(partition_1.default(restMalFormedCandidates, function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.ERROR; }), 2), errorCandidates = _c[0], restErrorCandidates = _c[1];
        var _d = tslib_1.__read(partition_1.default(restErrorCandidates, function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.OK; }), 2), okCandidates = _d[0], restOKCandidates = _d[1];
        var _e = tslib_1.__read(partition_1.default(restOKCandidates, function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.DELETED; }), 2), deletedCandidates = _e[0], notFoundCandidates = _e[1];
        return tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(sortBy_1.default(noPermissionCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(malFormedCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(errorCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(okCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(deletedCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(unAppliedCandidates, ['source_name', 'location']))), tslib_1.__read(sortBy_1.default(notFoundCandidates, ['source_name', 'location'])));
    };
    DebugImageDetails.prototype.getCandidates = function () {
        var _a = this.state, debugFiles = _a.debugFiles, loading = _a.loading;
        var image = this.props.image;
        var _b = (image !== null && image !== void 0 ? image : {}).candidates, candidates = _b === void 0 ? [] : _b;
        if (!debugFiles || loading) {
            return candidates;
        }
        var debugFileCandidates = candidates.map(function (_a) {
            var location = _a.location, candidate = tslib_1.__rest(_a, ["location"]);
            return (tslib_1.__assign(tslib_1.__assign({}, candidate), { location: (location === null || location === void 0 ? void 0 : location.includes(utils_3.INTERNAL_SOURCE_LOCATION))
                    ? location.split(utils_3.INTERNAL_SOURCE_LOCATION)[1]
                    : location }));
        });
        var candidateLocations = new Set(debugFileCandidates.map(function (_a) {
            var location = _a.location;
            return location;
        }).filter(function (location) { return !!location; }));
        var _c = tslib_1.__read(partition_1.default(debugFiles, function (debugFile) { return !candidateLocations.has(debugFile.id); }), 2), unAppliedDebugFiles = _c[0], appliedDebugFiles = _c[1];
        var unAppliedCandidates = unAppliedDebugFiles.map(function (debugFile) {
            var _a;
            var data = debugFile.data, symbolType = debugFile.symbolType, filename = debugFile.objectName, location = debugFile.id, size = debugFile.size, dateCreated = debugFile.dateCreated, cpuName = debugFile.cpuName;
            var features = (_a = data === null || data === void 0 ? void 0 : data.features) !== null && _a !== void 0 ? _a : [];
            return {
                download: {
                    status: debugImage_1.CandidateDownloadStatus.UNAPPLIED,
                    features: {
                        has_sources: features.includes(debugFiles_1.DebugFileFeature.SOURCES),
                        has_debug_info: features.includes(debugFiles_1.DebugFileFeature.DEBUG),
                        has_unwind_info: features.includes(debugFiles_1.DebugFileFeature.UNWIND),
                        has_symbols: features.includes(debugFiles_1.DebugFileFeature.SYMTAB),
                    },
                },
                cpuName: cpuName,
                location: location,
                filename: filename,
                size: size,
                dateCreated: dateCreated,
                symbolType: symbolType,
                fileType: utils_1.getFileType(debugFile),
                source: utils_3.INTERNAL_SOURCE,
                source_name: locale_1.t('Sentry'),
            };
        });
        var _d = tslib_1.__read(partition_1.default(debugFileCandidates, function (debugFileCandidate) {
            return debugFileCandidate.download.status === debugImage_1.CandidateDownloadStatus.OK &&
                debugFileCandidate.source === utils_3.INTERNAL_SOURCE;
        }), 2), debugFileInternalOkCandidates = _d[0], debugFileOtherCandidates = _d[1];
        var convertedDebugFileInternalOkCandidates = debugFileInternalOkCandidates.map(function (debugFileOkCandidate) {
            var internalDebugFileInfo = appliedDebugFiles.find(function (appliedDebugFile) { return appliedDebugFile.id === debugFileOkCandidate.location; });
            if (!internalDebugFileInfo) {
                return tslib_1.__assign(tslib_1.__assign({}, debugFileOkCandidate), { download: tslib_1.__assign(tslib_1.__assign({}, debugFileOkCandidate.download), { status: debugImage_1.CandidateDownloadStatus.DELETED }) });
            }
            var symbolType = internalDebugFileInfo.symbolType, filename = internalDebugFileInfo.objectName, location = internalDebugFileInfo.id, size = internalDebugFileInfo.size, dateCreated = internalDebugFileInfo.dateCreated, cpuName = internalDebugFileInfo.cpuName;
            return tslib_1.__assign(tslib_1.__assign({}, debugFileOkCandidate), { cpuName: cpuName, location: location, filename: filename, size: size, dateCreated: dateCreated, symbolType: symbolType, fileType: utils_1.getFileType(internalDebugFileInfo) });
        });
        return this.sortCandidates(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(convertedDebugFileInternalOkCandidates)), tslib_1.__read(debugFileOtherCandidates)), unAppliedCandidates);
    };
    DebugImageDetails.prototype.getDebugFilesSettingsLink = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, image = _a.image;
        var orgSlug = organization.slug;
        var debugId = image === null || image === void 0 ? void 0 : image.debug_id;
        if (!orgSlug || !projectId || !debugId) {
            return undefined;
        }
        return "/settings/" + orgSlug + "/projects/" + projectId + "/debug-symbols/?query=" + debugId;
    };
    DebugImageDetails.prototype.renderBody = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, image = _a.image, organization = _a.organization, projectId = _a.projectId, onReprocessEvent = _a.onReprocessEvent, event = _a.event;
        var _b = this.state, loading = _b.loading, builtinSymbolSources = _b.builtinSymbolSources;
        var _c = image !== null && image !== void 0 ? image : {}, code_file = _c.code_file, status = _c.status;
        var debugFilesSettingsLink = this.getDebugFilesSettingsLink();
        var candidates = this.getCandidates();
        var baseUrl = this.api.baseUrl;
        var fileName = utils_2.getFileName(code_file);
        var haveCandidatesUnappliedDebugFile = candidates.some(function (candidate) { return candidate.download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED; });
        var hasReprocessWarning = haveCandidatesUnappliedDebugFile &&
            displayReprocessEventAction_1.displayReprocessEventAction(organization.features, event) &&
            !!onReprocessEvent;
        return (<react_1.Fragment>
        <Header closeButton>
          <Title>
            {locale_1.t('Image')}
            <FileName>{fileName !== null && fileName !== void 0 ? fileName : locale_1.t('Unknown')}</FileName>
          </Title>
        </Header>
        <Body>
          <Content>
            <generalInfo_1.default image={image}/>
            {hasReprocessWarning && (<alertLink_1.default priority="warning" size="small" onClick={onReprocessEvent} withoutMarginBottom>
                {locale_1.t('You’ve uploaded new debug files. Reprocess events in this issue to view a better stack trace')}
              </alertLink_1.default>)}
            <candidates_1.default imageStatus={status} candidates={candidates} organization={organization} projectId={projectId} baseUrl={baseUrl} isLoading={loading} eventDateReceived={event.dateReceived} builtinSymbolSources={builtinSymbolSources} onDelete={this.handleDelete} hasReprocessWarning={hasReprocessWarning}/>
          </Content>
        </Body>
        <Footer>
          <StyledButtonBar gap={1}>
            <button_1.default href="https://docs.sentry.io/platforms/native/data-management/debug-files/" external>
              {locale_1.t('Read the docs')}
            </button_1.default>
            {debugFilesSettingsLink && (<button_1.default title={locale_1.t('Search for this debug file in all images for the %s project', projectId)} to={debugFilesSettingsLink}>
                {locale_1.t('Open in Settings')}
              </button_1.default>)}
          </StyledButtonBar>
        </Footer>
      </react_1.Fragment>);
    };
    return DebugImageDetails;
}(asyncComponent_1.default));
exports.default = DebugImageDetails;
var Content = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space_1.default(3), function (p) { return p.theme.fontSizeMedium; });
var Title = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"])), space_1.default(1), function (p) { return p.theme.fontSizeExtraLarge; });
var FileName = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
exports.modalCss = react_2.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  [role='document'] {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    width: 90%;\n  }\n\n  @media (min-width: ", ") {\n    width: 70%;\n  }\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"], ["\n  [role='document'] {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    width: 90%;\n  }\n\n  @media (min-width: ", ") {\n    width: 70%;\n  }\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"])), theme_1.default.breakpoints[0], theme_1.default.breakpoints[3], theme_1.default.breakpoints[4]);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map