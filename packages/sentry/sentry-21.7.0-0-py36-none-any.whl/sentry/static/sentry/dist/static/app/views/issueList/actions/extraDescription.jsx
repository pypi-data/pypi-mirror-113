Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var utils_1 = require("./utils");
function ExtraDescription(_a) {
    var all = _a.all, query = _a.query, queryCount = _a.queryCount;
    if (!all) {
        return null;
    }
    if (query) {
        return (<div>
        <p>{locale_1.t('This will apply to the current search query') + ':'}</p>
        <pre>{query}</pre>
      </div>);
    }
    return (<p className="error">
      <strong>
        {queryCount > utils_1.BULK_LIMIT
            ? locale_1.tct('This will apply to the first [bulkNumber] issues matched in this project!', {
                bulkNumber: utils_1.BULK_LIMIT_STR,
            })
            : locale_1.tct('This will apply to all [bulkNumber] issues matched in this project!', {
                bulkNumber: queryCount,
            })}
      </strong>
    </p>);
}
exports.default = ExtraDescription;
//# sourceMappingURL=extraDescription.jsx.map