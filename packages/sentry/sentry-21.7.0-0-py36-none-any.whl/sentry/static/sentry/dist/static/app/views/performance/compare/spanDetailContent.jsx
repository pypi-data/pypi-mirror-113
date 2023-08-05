Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var map_1 = tslib_1.__importDefault(require("lodash/map"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var spanDetail_1 = require("app/components/events/interfaces/spans/spanDetail");
var types_1 = require("app/components/events/interfaces/spans/types");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var SpanDetailContent = function (props) {
    var _a, _b;
    var span = props.span;
    var startTimestamp = span.start_timestamp;
    var endTimestamp = span.timestamp;
    var duration = (endTimestamp - startTimestamp) * 1000;
    var durationString = duration.toFixed(3) + "ms";
    var unknownKeys = Object.keys(span).filter(function (key) {
        return !types_1.rawSpanKeys.has(key);
    });
    return (<spanDetail_1.SpanDetails>
      <table className="table key-value">
        <tbody>
          <spanDetail_1.Row title={locale_1.t('Span ID')}>{span.span_id}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Parent Span ID')}>{span.parent_span_id || ''}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Trace ID')}>{span.trace_id}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Description')}>{(_a = span === null || span === void 0 ? void 0 : span.description) !== null && _a !== void 0 ? _a : ''}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Start Date')}>
            {getDynamicText_1.default({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<react_1.Fragment>
                  <dateTime_1.default date={startTimestamp * 1000}/>
                  {" (" + startTimestamp + ")"}
                </react_1.Fragment>),
        })}
          </spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('End Date')}>
            {getDynamicText_1.default({
            fixed: 'Mar 16, 2020 9:10:13 AM UTC',
            value: (<react_1.Fragment>
                  <dateTime_1.default date={endTimestamp * 1000}/>
                  {" (" + endTimestamp + ")"}
                </react_1.Fragment>),
        })}
          </spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Duration')}>{durationString}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Operation')}>{span.op || ''}</spanDetail_1.Row>
          <spanDetail_1.Row title={locale_1.t('Same Process as Parent')}>
            {String(!!span.same_process_as_parent)}
          </spanDetail_1.Row>
          <spanDetail_1.Tags span={span}/>
          {map_1.default((_b = span === null || span === void 0 ? void 0 : span.data) !== null && _b !== void 0 ? _b : {}, function (value, key) { return (<spanDetail_1.Row title={key} key={key}>
              {JSON.stringify(value, null, 4) || ''}
            </spanDetail_1.Row>); })}
          {unknownKeys.map(function (key) { return (<spanDetail_1.Row title={key} key={key}>
              {JSON.stringify(span[key], null, 4) || ''}
            </spanDetail_1.Row>); })}
        </tbody>
      </table>
    </spanDetail_1.SpanDetails>);
};
exports.default = SpanDetailContent;
//# sourceMappingURL=spanDetailContent.jsx.map