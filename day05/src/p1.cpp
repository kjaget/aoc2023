#include <algorithm>
#include <optional>
#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
#include <limits>
#include <thread>

std::vector<unsigned long> readNumbers(std::string line)
{
    std::vector<unsigned long> ret;
    const char * const delimiter{" "};
    char *savePtr;
    char const *token{strtok_r(line.data(), delimiter, &savePtr)};

    while (nullptr != token)
    {
        ret.push_back(atol(token));
        token = strtok_r(nullptr, delimiter, &savePtr);
    }
    return ret;
}

// Store the output seed location for a given input seed 
// along with the increment to get to the end of the
// range in which that seed matched
class RangeResult
{
public:
    constexpr RangeResult(unsigned long seed, unsigned long increment)
        : m_seed{seed}
        , m_increment{increment}
    {
    }
    unsigned long m_seed;
    unsigned long m_increment;
};

class Range
{
public:
    Range(unsigned long outputStart, unsigned long inputStart, unsigned long size)
        : m_outputStart{outputStart}
        , m_inputStart{inputStart}
        , m_size{size}
    {
    }

    // Given the input seed, see if it falls within this range
    // If so, return the remapped output seed value along with
    // the increment from that value to get to the end of the range
    std::optional<RangeResult> doMapping(const unsigned long input) const
    {
        if (input < m_inputStart || (input >= m_inputStart + m_size))
        {
            return std::nullopt;
        }
        //std::cout << "    Matched " << input << " against " << m_inputStart << " and " << m_inputStart + m_size << std::endl;
        return RangeResult{m_outputStart + (input - m_inputStart), m_size - (input - m_inputStart)};
    }

private:
    unsigned long m_outputStart;
    unsigned long m_inputStart;
    unsigned long m_size;

};

class RangeMap
{
public:
    explicit RangeMap(std::ifstream &istream)
    {
        std::string line;
        while (getline(istream, line) && !line.empty() && (line.find(":") == std::string::npos))
        {
            auto numbers = readNumbers(line);
            m_ranges.emplace_back(numbers[0], numbers[1], numbers[2]);
        }
    }
    // Search through all ranges in the map to see if the input seed
    // falls within any of them.  If so, return that range's output
    // which includes the remapped seed along with the increment
    // to get to the end of that range.
    // The input doesn't fall in any of the ranges, return the input
    // unmodified and an increment of 1.
    RangeResult doMapping(const unsigned long input) const
    {
        for (const auto &range : m_ranges)
        {
            //std::cout << "Testing " << input << std::endl;
            const auto output = range.doMapping(input);
            if (output.has_value())
            {
                //std::cout << "Matched " << input << " to " << output.value().m_value << std::endl;
                return output.value();
            }
        }
        return RangeResult{input, input + 1};
    }
private:
    std::vector<Range> m_ranges;
};

void seedWorker(const unsigned long start,
                const unsigned long size,
                const std::vector<RangeMap> &rangeMaps,
                unsigned long &minValue)
{
    struct SeedResult
    {
        SeedResult(unsigned long seed, unsigned long increment)
            : m_seed{seed}
            , m_increment{increment}
        {
        }
        unsigned long m_seed;
        unsigned long m_increment;
    };
    // Loop over all the maps in rangeMaps, applying the
    // remapping for each map in sequence to the input seed
    // Keep track of the min increment to the end of each range.
    // This is used to increment the seed value to the next
    // one to test. Values increse within a range, there's
    // no point in searching within the smallest range,
    // since output from that are guaranteed to be larger
    // that the current result.
    // Instead, increment one past the end of the smallest
    // range and continue the search there.
    auto calcSeed = [&rangeMaps](unsigned long seed)
    {
        SeedResult result{seed, std::numeric_limits<unsigned long>::max()};
        for (const auto &rangeMap : rangeMaps)
        {
            //std::cout << result.m_seed << " -> ";
            auto mappingResult = rangeMap.doMapping(result.m_seed);
            //std::cout << "   " << mappingResult.m_value << " increment = " << mappingResult.m_increment << std::endl;
            result = SeedResult{mappingResult.m_seed, std::min(mappingResult.m_increment, result.m_increment)};
        }
        //std::cout << seed << std::endl;
        return result;
    };

    unsigned long localMinValue = std::numeric_limits<unsigned long>::max();

    // Search over a range of seeds, starting at start and
    // incementing each time to get just past the end of the
    // smallest range which this seed maps to in any of the
    // range maps. This avoids searching higher numbers within
    // a range - since we're looking for the min value, no point
    // interating through higher values within a range.
    SeedResult result{std::numeric_limits<unsigned long>::max(), 1};
    for (size_t s = start; s < (start + size); s += result.m_increment)
    {
        result = calcSeed(s);
        localMinValue = std::min(result.m_seed, localMinValue);
    }
    //std::cout << "Finished " << start << " to " << (start + size) << " with min value " << localMinValue << std::endl;
    minValue = localMinValue;
}

int main(int argc, char *argv[])    
{
    std::ifstream istream(argv[1], std::ifstream::in);
    std::string line;
    getline(istream, line);
    const std::string seedStr = line.substr(line.find(":") + 2);
    std::vector<unsigned long> seeds{readNumbers(seedStr)};
    // Get blank line plus first map header
    getline(istream, line);
    getline(istream, line);

    std::vector<RangeMap> rangeMaps;
    do
    {
        rangeMaps.emplace_back(istream);
    }
    while (getline(istream, line));

    unsigned long minValue = std::numeric_limits<unsigned long>::max();
    for (const auto s : seeds)
    {
        unsigned long thisMinValue;
        seedWorker(s, 1, rangeMaps, thisMinValue);
        //std::cout << "Min value for seed " << s << " is " << thisMinValue << std::endl;
        minValue = std::min(thisMinValue, minValue);
    }

    std::cout << minValue << std::endl;

    std::vector<unsigned long> minValues;
    minValues.resize(seeds.size() / 2);
    std::vector<std::jthread> threads;
    for (size_t i = 0; i < seeds.size(); i += 2)
    {
        threads.emplace_back(seedWorker, seeds[i], seeds[i + 1], std::ref(rangeMaps), std::ref(minValues[i / 2]));
    }
    for (auto &thread : threads)
    {
        thread.join();
    }
    minValue = std::ranges::min(minValues);

    std::cout << minValue << std::endl;
    return 0;
}