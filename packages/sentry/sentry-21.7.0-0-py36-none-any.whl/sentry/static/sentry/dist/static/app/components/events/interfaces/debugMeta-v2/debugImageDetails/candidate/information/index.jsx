Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var debugImage_1 = require("app/types/debugImage");
var item_1 = tslib_1.__importDefault(require("../../../processing/item"));
var list_1 = tslib_1.__importDefault(require("../../../processing/list"));
var utils_1 = require("../../utils");
var divider_1 = tslib_1.__importDefault(require("./divider"));
var features_1 = tslib_1.__importDefault(require("./features"));
var processingIcon_1 = tslib_1.__importDefault(require("./processingIcon"));
function Information(_a) {
    var candidate = _a.candidate, isInternalSource = _a.isInternalSource, hasReprocessWarning = _a.hasReprocessWarning, eventDateReceived = _a.eventDateReceived;
    var source_name = candidate.source_name, source = candidate.source, location = candidate.location, download = candidate.download;
    function getFilenameOrLocation() {
        if (candidate.download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED ||
            (candidate.download.status === debugImage_1.CandidateDownloadStatus.OK && isInternalSource)) {
            var _a = candidate, symbolType = _a.symbolType, filename = _a.filename;
            return symbolType === debugImage_1.SymbolType.PROGUARD && filename === 'proguard-mapping'
                ? null
                : filename;
        }
        if (location && !isInternalSource) {
            return location;
        }
        return null;
    }
    function getTimeSinceData(dateCreated) {
        var dateTime = <dateTime_1.default date={dateCreated}/>;
        if (candidate.download.status !== debugImage_1.CandidateDownloadStatus.UNAPPLIED) {
            return {
                tooltipDesc: dateTime,
                displayIcon: false,
            };
        }
        var uploadedBeforeEvent = moment_timezone_1.default(dateCreated).isBefore(eventDateReceived);
        if (uploadedBeforeEvent) {
            if (hasReprocessWarning) {
                return {
                    tooltipDesc: (<React.Fragment>
              {locale_1.tct('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate. To apply new debug information, reprocess this issue.', {
                            when: moment_timezone_1.default(eventDateReceived).from(dateCreated, true),
                        })}
              <DateTimeWrapper>{dateTime}</DateTimeWrapper>
            </React.Fragment>),
                    displayIcon: true,
                };
            }
            var uplodadedMinutesDiff = moment_timezone_1.default(eventDateReceived).diff(dateCreated, 'minutes');
            if (uplodadedMinutesDiff >= 60) {
                return {
                    tooltipDesc: dateTime,
                    displayIcon: false,
                };
            }
            return {
                tooltipDesc: (<React.Fragment>
            {locale_1.tct('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate.', {
                        when: moment_timezone_1.default(eventDateReceived).from(dateCreated, true),
                    })}
            <DateTimeWrapper>{dateTime}</DateTimeWrapper>
          </React.Fragment>),
                displayIcon: true,
            };
        }
        if (hasReprocessWarning) {
            return {
                tooltipDesc: (<React.Fragment>
            {locale_1.tct('This debug file was uploaded [when] after this event. To apply new debug information, reprocess this issue.', {
                        when: moment_timezone_1.default(dateCreated).from(eventDateReceived, true),
                    })}
            <DateTimeWrapper>{dateTime}</DateTimeWrapper>
          </React.Fragment>),
                displayIcon: true,
            };
        }
        return {
            tooltipDesc: (<React.Fragment>
          {locale_1.tct('This debug file was uploaded [when] after this event.', {
                    when: moment_timezone_1.default(eventDateReceived).from(dateCreated, true),
                })}
          <DateTimeWrapper>{dateTime}</DateTimeWrapper>
        </React.Fragment>),
            displayIcon: true,
        };
    }
    function renderProcessingInfo() {
        if (candidate.download.status !== debugImage_1.CandidateDownloadStatus.OK &&
            candidate.download.status !== debugImage_1.CandidateDownloadStatus.DELETED) {
            return null;
        }
        var items = [];
        var _a = candidate, debug = _a.debug, unwind = _a.unwind;
        if (debug) {
            items.push(<item_1.default key="symbolication" type="symbolication" icon={<processingIcon_1.default processingInfo={debug}/>}/>);
        }
        if (unwind) {
            items.push(<item_1.default key="stack_unwinding" type="stack_unwinding" icon={<processingIcon_1.default processingInfo={unwind}/>}/>);
        }
        if (!items.length) {
            return null;
        }
        return (<React.Fragment>
        <StyledProcessingList items={items}/>
        <divider_1.default />
      </React.Fragment>);
    }
    function renderExtraDetails() {
        if ((candidate.download.status !== debugImage_1.CandidateDownloadStatus.UNAPPLIED &&
            candidate.download.status !== debugImage_1.CandidateDownloadStatus.OK) ||
            source !== utils_1.INTERNAL_SOURCE) {
            return null;
        }
        var _a = candidate, symbolType = _a.symbolType, fileType = _a.fileType, cpuName = _a.cpuName, size = _a.size, dateCreated = _a.dateCreated;
        var _b = getTimeSinceData(dateCreated), tooltipDesc = _b.tooltipDesc, displayIcon = _b.displayIcon;
        return (<React.Fragment>
        <tooltip_1.default title={tooltipDesc}>
          <TimeSinceWrapper>
            {displayIcon && <icons_1.IconWarning color="red300" size="xs"/>}
            {locale_1.tct('Uploaded [timesince]', {
                timesince: <timeSince_1.default disabledAbsoluteTooltip date={dateCreated}/>,
            })}
          </TimeSinceWrapper>
        </tooltip_1.default>
        <divider_1.default />
        <fileSize_1.default bytes={size}/>
        <divider_1.default />
        <span>
          {symbolType === debugImage_1.SymbolType.PROGUARD && cpuName === 'any'
                ? locale_1.t('proguard mapping')
                : "" + symbolType + (fileType ? " " + fileType : '')}
        </span>
        <divider_1.default />
      </React.Fragment>);
    }
    var filenameOrLocation = getFilenameOrLocation();
    return (<Wrapper>
      <div>
        <strong data-test-id="source_name">
          {source_name ? capitalize_1.default(source_name) : locale_1.t('Unknown')}
        </strong>
        {filenameOrLocation && (<FilenameOrLocation>{filenameOrLocation}</FilenameOrLocation>)}
      </div>
      <Details>
        {renderExtraDetails()}
        {renderProcessingInfo()}
        <features_1.default download={download}/>
      </Details>
    </Wrapper>);
}
exports.default = Information;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  max-width: 100%;\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  max-width: 100%;\n"])));
var FilenameOrLocation = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  font-size: ", ";\n"], ["\n  padding-left: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeSmall; });
var Details = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeSmall; });
var TimeSinceWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(0.5));
var DateTimeWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space_1.default(1));
var StyledProcessingList = styled_1.default(list_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map