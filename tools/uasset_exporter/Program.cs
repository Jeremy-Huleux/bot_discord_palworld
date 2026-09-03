using System.Text.Json;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.UnrealTypes;

if (args.Length < 2)
{
    Console.Error.WriteLine("Usage: UAssetExporter <input-root> <output-root> [engine-version]");
    return 2;
}

var inputRoot = Path.GetFullPath(args[0]);
var outputRoot = Path.GetFullPath(args[1]);
var engineVersion = args.Length > 2
    ? Enum.Parse<EngineVersion>(args[2], ignoreCase: false)
    : EngineVersion.VER_UE5_1;

if (!Directory.Exists(inputRoot))
{
    Console.Error.WriteLine($"Input directory not found: {inputRoot}");
    return 2;
}

var assets = Directory.EnumerateFiles(inputRoot, "*.uasset", SearchOption.AllDirectories)
    .Where(path => !path.Contains("/L10N/", StringComparison.OrdinalIgnoreCase))
    .Where(path => Path.GetFileName(path).StartsWith("DT_", StringComparison.OrdinalIgnoreCase))
    .OrderBy(path => path, StringComparer.Ordinal)
    .ToList();

var exported = 0;
var skipped = 0;
foreach (var assetPath in assets)
{
    try
    {
        var asset = new UAsset(assetPath, true, engineVersion);
        var table = asset.Exports.OfType<DataTableExport>().FirstOrDefault();
        if (table is null)
        {
            skipped++;
            continue;
        }

        var rows = new Dictionary<string, JsonElement>(StringComparer.Ordinal);
        var names = asset.GetNameMapIndexList()
                 .Select(value => value.ToString())
                 .Distinct(StringComparer.Ordinal)
                 .ToList();
        foreach (var name in names)
        {
            var row = table[name];
            if (row is null)
            {
                continue;
            }

            using var rowDocument = JsonDocument.Parse(asset.SerializeJsonObject(row, false));
            rows[name] = rowDocument.RootElement.Clone();
        }

        var relativePath = Path.GetRelativePath(inputRoot, assetPath);
        var outputPath = Path.Combine(outputRoot, Path.ChangeExtension(relativePath, ".json"));
        Directory.CreateDirectory(Path.GetDirectoryName(outputPath)!);
        var payload = new
        {
            source_asset = relativePath.Replace(Path.DirectorySeparatorChar, '/'),
            engine_version = engineVersion.ToString(),
            row_count = rows.Count,
            rows,
        };
        var json = JsonSerializer.Serialize(payload, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(outputPath, json + Environment.NewLine);
        exported++;
        Console.WriteLine($"exported {relativePath} rows={rows.Count}");
    }
    catch (Exception error)
    {
        skipped++;
        Console.Error.WriteLine($"skipped {Path.GetRelativePath(inputRoot, assetPath)}: {error.GetType().Name}: {error.Message}");
    }
}

Console.WriteLine($"summary exported={exported} skipped={skipped} assets={assets.Count}");
return skipped == 0 ? 0 : 1;
