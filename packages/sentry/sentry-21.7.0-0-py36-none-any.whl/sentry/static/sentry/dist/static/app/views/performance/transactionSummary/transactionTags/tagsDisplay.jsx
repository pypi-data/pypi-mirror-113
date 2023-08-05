Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var react_2 = require("@emotion/react");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var segmentExplorerQuery_1 = tslib_1.__importDefault(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
var tagKeyHistogramQuery_1 = tslib_1.__importDefault(require("app/utils/performance/segmentExplorer/tagKeyHistogramQuery"));
var filter_1 = require("../filter");
var tagExplorer_1 = require("../tagExplorer");
var tagsHeatMap_1 = tslib_1.__importDefault(require("./tagsHeatMap"));
var tagValueTable_1 = require("./tagValueTable");
var HISTOGRAM_TAG_KEY_LIMIT = 8;
var HISTOGRAM_BUCKET_LIMIT = 20;
var TagsDisplay = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, tagKey = props.tagKey;
    var aggregateColumn = tagExplorer_1.getTransactionField(filter_1.SpanOperationBreakdownFilter.None, projects, eventView);
    return (<react_1.default.Fragment>
      {tagKey ? (<react_1.default.Fragment>
          <tagKeyHistogramQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} tagKeyLimit={HISTOGRAM_TAG_KEY_LIMIT} numBucketsPerKey={HISTOGRAM_BUCKET_LIMIT} tagKey={tagKey} sort="-frequency">
            {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData;
                return (<tagsHeatMap_1.default {...props} tagKey={tagKey} aggregateColumn={aggregateColumn} tableData={tableData} isLoading={isLoading}/>);
            }}
          </tagKeyHistogramQuery_1.default>
          <segmentExplorerQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} tagKey={tagKey} limit={HISTOGRAM_TAG_KEY_LIMIT} sort="-frequency" allTagKeys>
            {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData;
                return (<tagValueTable_1.TagValueTable {...props} tagKey={tagKey} aggregateColumn={aggregateColumn} tableData={tableData} isLoading={isLoading}/>);
            }}
          </segmentExplorerQuery_1.default>
        </react_1.default.Fragment>) : (<placeholder_1.default height="290"/>)}
    </react_1.default.Fragment>);
};
exports.default = react_2.withTheme(TagsDisplay);
//# sourceMappingURL=tagsDisplay.jsx.map